# Treep, copyright 2019 Max Planck Gesellschaft
# Author : Vincent Berenz 

# This file is part of Treep.

#    Treep is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    Treep is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with Treep.  If not, see <https://www.gnu.org/licenses/>.


from __future__ import print_function

import os,time

from . import multiprocess
from . import treep_git
from . import status
from . import coloring
from .console_manager import Console_manager
from .compiler import Compiler
from .interactive import interactive_execute
from .process_calls import execute
from .ssh import get_host, authenticity_of_host_is_established

class UnknownProject(Exception):
    pass

class UnknownRepository(Exception):
    pass


INFO=-1
ERROR = 0
WARNING = 1
OK = 2


class Projects :


    def __init__( self,
                  projects, # dict {project name : project instance}
                  repositories, # dict {repo name : repo instance}
                  ordered_repositories, # list [repo name], in ordered declared in config file
                  compiler,
                  workspace_path,
                  conflicts_projects,
                  conflicts_repositories ):

        self._projects = projects
        self._repositories = repositories
        self._ordered_repositories = ordered_repositories
        self._workspace_path = workspace_path
        self._conflicts_projects = conflicts_projects
        self._conflicts_repositories = conflicts_repositories
        self._compiler = compiler


    # some projects are used in the configuration
    # (as parent of other projects), but are undefined
    # (because possibly defined in another treep configuration
    # folder that is not in the workspace)
    def missing_parent_projects( self,
                                 project_name,
                                 missing=set() ) :

        missing_ = set([m for m in missing])
        missing = set()
        
        project = self.get_project(project_name)

        project_names = [project_.name for project_ in self._projects.values()]

        for parent_project in project.parent_projects:
            if parent_project not in missing:
                if parent_project not in project_names:
                    missing.add(parent_project)
                else :
                    self.missing_parent_projects(parent_project,missing=missing)

        return missing_

    # some repos are used in the configuration, but are undefined,
    # (possibly because defined in another treep configuration
    # folder that is not in the workspace)
    def missing_repositories( self,
                              project_name,
                              missing=set(),
                              missing_parents=None ):

        missing_ = set([m for m in missing])
        missing = set()
        
        if missing_parents is None:
            missing_parents = self.missing_parent_projects(project_name)

        project = self.get_project(project_name)

        for repository in project.repositories:
            if repository not in self._repositories:
                missing_.add(repository)

        for parent in [ p for p in project.parent_projects
                        if p not in missing_parents ] :

            self.missing_repositories( parent,
                                       missing=missing_,
                                       missing_parents=missing_parents )

        return missing_
        

    # repo_names is an unordered list of repos,
    # this function returnes the ordered content
    # of repo_names, order in the order of declaration
    # of the config files (which is an indication in
    # which order the related cmake packages should be
    # compiled)
    def order_repositories(self,repo_names):
        ordered_repositories = {repo.name:index for index,repo in enumerate(self._ordered_repositories)}
        repo_names = sorted(repo_names,key = lambda repo: ordered_repositories[repo])
        return repo_names
        
    def generate_compilation_script(self,
                                    project_or_repo_name,
                                    config={},
                                    raise_exception=False,
                                    interactive=True):

        if project_or_repo_name is None:
            repos = self.get_cloned_repos()
        elif project_or_repo_name in self._projects.keys() :
            repos = self.get_repos(project_or_repo_name)
        else :
            if project_or_repo_name not in self._repositories.keys():
                raise UnknownRepository(project_or_repo_name)
            repos = [project_or_repo_name]

        
        # compilation script will be printed in treep root folder
        target_directory = os.path.abspath(self.get_workspace_path()+"..")+os.sep
        
        try :
        
            repo_names = repos

            repos = [ self._repositories[repo_name]
                      for repo_name in repo_names ]
            
            # filtering repo with no compilation attribute
            repos = [repo for repo in repos if repo.compilation is not None]

            # splitting repos into compilation type
            
            repos_ = {compilation_type:[] for compilation_type in Compiler.COMPILATION_TYPES}
            for repo in repos:
                repos_[self._compiler.configurations[repo.compilation][0]].append(repo.name)
            repos = repos_
                
            # ensuring compilation will be done in the order specified
            # in the yaml config file
            repos_ = {}
            for compilation_type,repo_list in repos.items():
                r = self.order_repositories([repo for repo in repo_list])
                repos_[compilation_type]=r
            repos = repos_
                
            # fully ordered list of repos
            repos_ = []
            for compilation_type in sorted(Compiler.COMPILATION_TYPES):
                try :
                    repo_list = repos[compilation_type]
                    repos_.extend(repo_list)
                except :
                    pass
            repos = repos_
                
            # going through all repo and updating compilation script
            # accordingly

            script = []
            functions = []
            
            for repo_name in repos:
                label = self._repositories[repo_name].compilation
                if label is not None:
                    path = self.get_repo_path(repo_name)

                    if not interactive:

                        # generating the script using yaml configuration arguments
                        
                        script_ = self._compiler.get_script(target_directory,
                                                            repo_name,
                                                            path,
                                                            label,
                                                            return_function=False)
                        script.append('echo ""\necho "* compiling '+repo_name+ ' * "\necho ""')
                        script.append(script_)

                    else :

                        # generating the script using user input
                        function = self._compiler.get_script(target_directory,
                                                             repo_name,
                                                             path,
                                                             label,
                                                             return_function=True)

                        functions.append(function)

            if not interactive:

                script = "\n\n".join(script)
                        
            if interactive :

                # the script has not been generated, just
                # the functions for generating it
                # while asking for user's inputs have been
                # collected

                script = interactive_execute(functions)
                        

            file_path =  target_directory+"compilation.sh"

            with open(file_path,"w+") as f:

                f.write("#! /bin/bash\n\n")
                f.write("\n# exit at first error\n")
                f.write("set -e\n\n") 
                f.write(script)
                f.write("\n")

            execute("chmod +x "+str(file_path))
                
            print("\n\tgenerated compilation file:\n\t"+coloring.b_green(file_path)+"\n")

        except Exception as e:

            if raise_exception:
                raise(e)
            
            print("\n"+coloring.red("\tfailed to generate compilation file:\n\t")+
                  coloring.orange(str(e))+"\n")
            
        return target_directory+"compilation.sh"
                
    def get_conflicts(self):
        return self._conflicts_repositories,self._conflicts_projects

    def display_conflicts(self):

        if not self.has_conflicts():
            print(coloring.b_green("\n\t\tno conflicts detected\n"))
            return

        if self._conflicts_repositories:
            print(coloring.b_orange("\t\tREPOSITORIES:"))
            for repo,folders in self._conflicts_repositories.items():
                print("\t\t\t"+coloring.cyan(repo)+" defined in "+", ".join(folders))
            print('')
            
        if self._conflicts_projects:
            print(coloring.b_orange("\t\tprojects:"))
            for project,folders in self._conflicts_projects.items():
                print("\t\t\t"+coloring.cyan(project)+" defined in "+", ".join(folders))
            print('')


            
    def has_conflicts(self):
        if len(self._conflicts_repositories) != 0:
            return True
        if len(self._conflicts_projects) != 0:
            return True
        return False

    def get_workspace_path(self):

        return self._workspace_path


    def get_nb_projects(self):

        return len(self._projects)

    
    def get_nb_repos(self):

        return len(self._repositories)
    
    
    def get_project(self,project_name):

        try :
            return self._projects[project_name]
        except :
            raise UnknownProject(project_name)


    def get_repo(self,repo_name):

        try :
            return self._repositories[repo_name]
        except :
            raise UnknownRepository(repo_name)


    def get_projects(self):
        for project in self._projects.values():
            yield project


    def get_projects_names(self):
        return self._projects.keys()

    
    def get_repos_names(self):
        return self._repositories.keys()


    def get_names(self):
        return list(self.get_projects_names()) + list(self.get_repos_names())
    
    def get_repos(self,project_name):

        if project_name is None:
            return self._repositories.values()

        parent_projects = set()

        def _add_parents(project_name,parents):
            parents.add(project_name)
            project = self.get_project(project_name)
            for parent_project in project.parent_projects:
                _add_parents(parent_project,parents)

        _add_parents(project_name,parent_projects)

        repos = set()

        for project_name in parent_projects:
            project = self.get_project(project_name)
            for repo in project.repositories:
                repos.add(repo)
                
        return repos


    def has_repo(self,project_name,repo_name):

        return repo_name in self.get_repos(project_name)


    def already_cloned(self,repo_name):

        repo = self.get_repo(repo_name)
        abs_path  = self.get_repo_path(repo_name)
        if os.path.isdir(abs_path):
            return True
        return False


    # returns tuple of 3 None if repo origin
    # does not start with git@
    # other wise returns tuple established,host name,origin
    # for the repo, established being false meaning
    # git clone with prompt for establishing authenticity
    # (prompting does not live well with the multithreading
    # cloning of treep)
    def check_ssh_authenticity(self,repo_name):

        repo = self.get_repo(repo_name)
        host = get_host(repo.origin)
        if host is None:
            return None,None,None
        established = authenticity_of_host_is_established(host)
        return established,host,repo.origin

    # returns dict repo name = (host,origin)
    # for repos which host can not be established
    # (hence will result in prompting during git clone)
    def check_ssh_authenticities(self,repo_names,console=True):

        not_established=set()
        checked = set()

        def get_hosts(repo_names):
            hosts = set()
            for repo_name in repo_names:
                repo = self.get_repo(repo_name)
                host = get_host(repo.origin)
                if host is not None:
                    hosts.add(host)
            return hosts

        hosts = get_hosts(repo_names)

        if hosts and console :
            print(coloring.dim("\tchecking authenticity of ssh git servers:"))
        for host in hosts:
            established = authenticity_of_host_is_established(host)
            if not established:
                not_established.add(host)
                if console:
                    print("\t\t",coloring.cyan(host)+" ... "+coloring.red('failed'))
            else:
                if console:
                    print("\t\t",coloring.cyan(host)+" ... "+coloring.green('ok'))
                        
        return not_established
                
    def pretty_print_repo(self,repo_name,nb_tabs=0):

        already_cloned = self.already_cloned(repo_name)
        repo = self.get_repo(repo_name)
        
        print ('\t'*(nb_tabs+2),end='')
        if already_cloned:
            print (coloring.b_green(repo_name),end='\t')
        else :
            print (coloring.dim(repo_name),end='\t')
        print (coloring.cyan(repo.origin),end='\t')
        print (coloring.dim(repo.path),end='\n')

        
            
    def pretty_print_project_tree(self,project_name,nb_tabs=1,printed_repos=None):
        
        project = self.get_project(project_name)
        printed_repos = set()
        nb_tabs_ = nb_tabs
        for parent_project in project.parent_projects:
            nb_tabs_ = self.pretty_print_project(parent_project,nb_tabs+1,printed_repos=printed_repos)
        nb_tabs_+=1
        print('\t'*nb_tabs_+coloring.b_cyan(project_name))
        for repo in project.repositories:
            if repo not in printed_repos:
                self.pretty_print_repo(repo,nb_tabs_)
                printed_repos.add(repo)
        return nb_tabs_

    
    def pretty_print_project(self,project_name,printed_projects=[]):
        
        project = self.get_project(project_name)
        printed_repos = set()
        for parent_project in project.parent_projects:
            if parent_project not in printed_projects:
                self.pretty_print_project(parent_project,
                                          printed_projects=printed_projects)
                printed_projects.append(parent_project)
        print('\t'+coloring.b_cyan(project_name))
        for repo in sorted(project.repositories):
            self.pretty_print_repo(repo)
            printed_repos.add(repo)
    
            
    def get_cloned_repos(self):

        r = []
        for repo_name in self._repositories.keys():
            if self.already_cloned(repo_name):
                r.append(repo_name)
        return sorted(r)

    
    def get_repos_paths(self,repo_names):

        r = {}
        for repo_name in repo_names:
            instance = self.get_repo(repo_name)
            absolute_path = self._workspace_path+instance.path+os.sep+instance.name
            r[repo_name] = absolute_path
        return r


    def get_repo_path(self,repo_name):

        return list(self.get_repos_paths([repo_name]).values())[0]


    # change the origins of repos to match the one provided in the
    # yaml configuration files. This may be useful if the configuration
    # files change, e.g. when moving repos from gitlab to github
    def fix_origins(self,console=True):

        repos = self.get_cloned_repos()
        
        if console:
            console_manager = Console_manager()
        
        for repo in repos:

            if console:
                print(coloring.b_green("\t"+repo))

            path = self.get_repo_path(repo)

            try :

                current_fetch_origin = treep_git.get_fetch_origin(path)
                if current_fetch_origin is None:
                    current_fetch_origin = "(invalid URL or access refused)"
                else :
                    current_fetch_origin = current_fetch_origin.strip()

                current_push_origin = treep_git.get_push_origin(path)
                if current_push_origin is None:
                    current_push_origin = "(invalid URL or access refused)"
                else :
                    current_push_origin = current_push_origin.strip()

                desired_origin = self._repositories[repo].origin.strip()

                if all([desired_origin==origin
                        for origin in [current_fetch_origin,
                                       current_push_origin]]):
                    if console:
                        print(coloring.dim("\t\tunchanged: "+desired_origin))

                else :

                    treep_git.set_origin(path,desired_origin)

                    if console:

                        if desired_origin!=current_fetch_origin:
                            print(coloring.cyan("\t\tupdated fetch origin: "))
                            print("\t\t\tprevious: "+current_fetch_origin)
                            print(coloring.green("\t\t\tnew: "+desired_origin))

                        if desired_origin!=current_push_origin:
                            print(coloring.cyan("\t\tupdated push origin: "))
                            print("\t\t\tprevious: "+current_push_origin)
                            print(coloring.green("\t\t\tnew: "+desired_origin))

            except Exception as e:
                
                print(coloring.red("\t\tERROR"))
                console_manager.add_error(repo,str(e))
        

        if console:
            console_manager.console()

        
    def add_and_commit(self,
                       project_or_repo_name,
                       commit_message,
                       console=True,
                       raise_exception=False):

        if console:
            console_manager = Console_manager()
            print(coloring.b_green("\n\tadding and commiting"))
        
        if project_or_repo_name is None:
            repos = self.get_cloned_repos()
        elif project_or_repo_name in self._projects.keys() :
            repos = self.get_repos(project_or_repo_name)
        else :
            if project_or_repo_name not in self._repositories.keys():
                raise UnknownRepository(project_or_repo_name)
            repos = [project_or_repo_name]

        for repo in repos:

            path = self.get_repo_path(repo)

            if console :
                print("\t\t"+coloring.cyan(repo)+" ... ",end='')

            local_modifications = treep_git.local_modifications(path)

            if not local_modifications:
                print (coloring.orange("no local modifications"))

            else :
                
                try :
                    nb_added = treep_git.add_all(path)
                    added = True
                except Exception as e:
                    added = False
                    if console:
                        print (coloring.red("ERROR"))
                        console_manager.add_error(repo,str(e))
                    else :
                        if raise_exception:
                            raise e

                if added :

                    try :
                        treep_git.commit(path,commit_message)
                        if console:
                            if nb_added == 0:
                                print (coloring.dim("no file added"))
                            else :
                                if nb_added == 1:
                                    file_ = "file"
                                else :
                                    file_ = "files"
                                print (coloring.green(str(nb_added)+" "+file_+" added"))

                    except Exception as e:
                        if console:
                            print (coloring.red("ERROR"))
                            console_manager.add_error(repo,str(e))
                        else :
                            if raise_exception:
                                raise e

        if console:
            console_manager.console()

            
    def push(self,
             project_or_repo_name,
             console=True,
             raise_exception=False):

        if console:
            console_manager = Console_manager()
            print(coloring.b_green("\n\tpushing"))
        
        if project_or_repo_name is None:
            repos = self.get_cloned_repos()
        elif project_or_repo_name in self._projects.keys() :
            repos = self.get_repos(project_or_repo_name)
        else :
            if project_or_repo_name not in self._repositories.keys():
                raise UnknownRepository(project_or_repo_name)
            repos = [project_or_repo_name]

        for repo in repos:

            path = self.get_repo_path(repo)
            
            if console :
                print("\t\t"+coloring.cyan(repo)+" ... ",end='')

            try :
                current_branch = treep_git.current_branch(path)
                treep_git.push_to_origin(path,current_branch)
                print (coloring.green("OK"))
            except Exception as e:
                if console:
                    print (coloring.red("ERROR"))
                    console_manager.add_error(repo,str(e))
                else :
                    if raise_exception:
                        raise e
                    
            
        if console:
            console_manager.console()


    def clone( self,
               project_or_repo_name=None,
               console=True,
               raise_exception=False,
               branch=True,
               commit=True,
               tag=True,
               run_multiprocess=True ):

        raise_exception_ = raise_exception
        raise_exception = False
        
        # some project can not be cloned because depending
        # on parent project or repo that are defined in another
        # treep configuration folder that is not in the workspace

        if project_or_repo_name is not None and project_or_repo_name in self._projects.keys():

            missing_parents = self.missing_parent_projects( project_or_repo_name )
            if missing_parents:
                if console:
                    print("\n\t"+coloring.red("can not clone "+project_or_repo_name))
                    print("\tthe following parent projects are unknown:")
                    print("\t"+" ".join(missing_parents))
                    print("\n")
                if raise_exception_:
                    raise Exception("\tcan not clone: "+project_or_repo_name
                                    +" because of unknown parent projects: "
                                    +" ".join(missing_parents))
                else:
                    return

            missing_repositories = self.missing_repositories( project_or_repo_name )
            if missing_repositories:
                if console:
                    print("\n\t"+coloring.red("can not clone "+project_or_repo_name))
                    print("\tthe following repositories are unknown:")
                    print("\t"+" ".join(missing_repositories))
                    print("\n")
                if raise_exception_:
                    raise Exception("\tcan not clone: "+project_or_repo_name
                                    +" because of unknown repositories: "
                                    +" ".join(missing_repositories))
                else:
                    return
            
        # all repos are cloned in workspace directory,
        # which is created here is not already there
        if not os.path.isdir(self._workspace_path):
            try :
                os.makedirs(self._workspace_path)
            except Exception as e:
                raise Exception("failed to create workspace "+
                                self._workspace_path+": "+str(e))

        # list of repos to clone
        if project_or_repo_name is None:
            # cloning all repos
            repos = self._repositories.keys()
        else :
            if project_or_repo_name in self._projects.keys() :
                repos = self.get_repos(project_or_repo_name)
            else :
                if project_or_repo_name not in self._repositories.keys():
                    raise UnknownRepository(project_or_repo_name)
                repos = [project_or_repo_name]

        # check for each repo if ssh cloning will be without
        # prompt. host_not_established is a dict [repo name]=(host,origin)
        # for repos which would prompt (these repos will not be cloned
        # by treep)
        hosts_not_established = self.check_ssh_authenticities(repos,console=console)

        if hosts_not_established:
            if raise_exception:
                raise Exception("authenticity of servers "+", ".join(hosts_not_established)+
                                " could not be established")
            if console:
                print("\n\t",
                      coloring.red("[ERROR]"),
                      "authenticity of at least one server could not be established.")
                print("\t",
                      coloring.dim("possible fix: clone manually a repo from this server to establish authenticity via prompt\n"))
        
        # informing user with start to clone
        if console:
            console_manager = Console_manager()
            print(coloring.b_green("\n\tcloning"))


        # creating config dict for earch repo
        repo_config = {}
        for repo in repos:
            config = {}
            config["name"]=repo
            instance = self.get_repo(repo)
            absolute_path = self.get_repo_path(repo)
            config["path"] = absolute_path
            if branch:
                config["branch"] = instance.branch
            else :
                config["branch"] = False
            if tag:
                config["tag"] = instance.tag
            else :
                config["tag"] = False
            if commit :
                config["commit"] = instance.commit
            else :
                config["commit"] = False
            config["already_cloned"] = self.already_cloned(repo)
            config["origin"] = instance.origin
            repo_config[repo]=config


        # function for cloning a single repo
        def _clone(shared_errors,
                   shared_lock,
                   config,
                   console,
                   raise_exception,
                   nb_attempts=0):

            output = []

            def _checkout(config,key,output):

                output.append(coloring.dim("\n\t\t\tchecking out "+
                                           coloring.b_green(str(key))+" "))
                output.append(coloring.cyan(config[key])+" ... ")

                if key=="branch" :
                    fn = treep_git.checkout_branch
                elif key=="commit" :
                    fn = treep_git.checkout_commit
                elif key=="tag" :
                    fn = treep_git.checkout_tag
                    
                try:
                    fn(config["path"],
                       config[key])
                    output.append(coloring.green("OK"))
                except Exception as e:
                    output.append(coloring.red("ERROR"))
                    shared_errors[config["name"]]= str("failed to checkout "
                                                       +str(config[key])
                                                       +": "+str(e))

            # attempt up to 20 cloning before giving up
            def _cloning(config,output,nb_attempts=0):

                try :

                    # repo not already in workspace, cloning
                    if not config["already_cloned"]:
                        treep_git.clone(config["origin"],config["path"])
                        treep_git.clone_submodules(config["path"])
                        if console:
                            output.append("\t\t"+coloring.cyan(config["name"])+" ... ")
                            output.append(coloring.green("OK"))

                    # repo already in workspace, not cloning again
                    else :
                        if console:
                            output.append("\t\t"+coloring.cyan(config["name"])+" ... ")
                            output.append(coloring.dim("already cloned"))
                         
                    # cloning worked, trying to checking out things
                    
                    # if required by the treep config, checking out
                    # branch/tag/commit if different from current one
                    status = self.get_status(config["name"],
                                             fetch_first=False,
                                             console=False)

                    # checking out branch
                    if config["branch"] and status.branch!=config["branch"]:
                        try:
                            _checkout(config,"branch",output)
                        except :
                            # shared error and output also
                            # updated when exception throw in checkout
                            pass
                      
                    # checking out the branch may have changed the
                    # status
                    status = self.get_status(config["name"],
                                             fetch_first=False,
                                             console=False)

                    # checking out commit
                    if config["commit"] and config["commit"]!=status.commit_sha1:
                        try:
                            _checkout(config,"commit",output)
                        except :
                            # shared error and output also
                            # updated when exception throw in checkout
                            pass

                    # checking out tag
                    if config["tag"] and config["tag"]!=status.commit_sha1:
                        try:
                            _checkout(config,"tag",output)
                        except :
                            # shared error and output also
                            # updated when exception throw in checkout
                            pass
                        
                except Exception as e :
                    if nb_attempts<20:
                        time.sleep(0.01)
                        _cloning(config,output,nb_attempts=nb_attempts+1)
                    else:
                        if console:
                            with shared_lock:
                                print ("\t\t"+coloring.cyan(config["name"])
                                       +coloring.dim(" ... ")+coloring.red(" ERROR"))
                            return False,str(e)
                        elif raise_exception :
                            raise e
                        
            _cloning(config,output)

            print("".join(output))


        # will execute all clone using multiprocesses
        executor = multiprocess.Multiprocess(run_multiprocess,
                                             _clone,
                                             console,
                                             raise_exception)
        errors = executor.execute(repo_config)

        
        # displaying errors that occured during clone
        for repo_name,error in errors.items():
                console_manager.add_error(repo_name,error)
        if console:
            console_manager.console()

        
            

    def pull( self,
              project_or_repo_name,
              console=True,
              raise_exception=False,
              run_multiprocess=True ):


        # function for pulling one repo
        def _pull( shared_errors,
                   shared_lock,
                   repo_config,
                   console,
                   raise_exception,
                   nb_attempts=0 ):

            prefix = "\t\t"+coloring.cyan(repo_config["name"])+" ... "

            try :

                # pulling
                out = treep_git.pull(repo_config["path"])

                if console:

                    # output of pulling shows that pulling failed.
                    # trying at least 10 times before giving up
                    if nb_attempts<10 and "fatal" and "Could not read" in out:
                        _pull(shared_errors,shared_lock,repo_config,
                              console,raise_exception,nb_attempts=nb_attempts+1)

                    # pulling worked ok
                    else :
                        with shared_lock:

                            # pull worked, but did nothing, dim output
                            if "up-to-date" in out:
                                
                                print (prefix+coloring.dim("(already up to date)"))

                            else:

                                print (prefix+coloring.green("OK"))
                                
                                # pull worked, but the repo was not updated
                                # orange output
                                if not "Updating" in out:
                                    color_fn = coloring.orange
                                # pull worked, and the repo was updated,
                                # normal output
                                else:
                                    color_fn = lambda v : v

                                    
                                out_str =  out[:-1].split('\n')
                                for line in out_str:
                                    line_ = line.strip()
                                    if line_:
                                        print(color_fn("\t\t\t"+str(line_)))



            except Exception as e :
                if nb_attempts<10:
                    _pull(shared_errors,shared_lock,repo_config,
                          console,raise_exception,nb_attempts=nb_attempts+1)
                else :
                    if console:
                        with shared_lock:
                            print (prefix+coloring.red("ERROR"))
                            shared_errors[repo_config["name"]]=str(e)
                    else :
                        if raise_exception:
                            raise e


        if console:
            console_manager = Console_manager()
            print(coloring.b_green("\n\tpulling"))

        # list of repos to pull
        if project_or_repo_name is None:
            repos = self.get_cloned_repos()
        elif project_or_repo_name in self._projects.keys() :
            repos = self.get_repos(project_or_repo_name)
        else :
            if project_or_repo_name not in self._repositories.keys():
                raise UnknownRepository(project_or_repo_name)
            repos = [project_or_repo_name]
        repo_config = {}
        for repo_name in repos:
            config = {}
            config["name"] = repo_name
            repo_config[repo_name] = {}
            instance = self.get_repo(repo_name)
            absolute_path = self.get_repo_path(repo_name)
            config["path"] = absolute_path
            repo_config[repo_name]=config


        # will execute all pulls using multiprocesses
        executor = multiprocess.Multiprocess(run_multiprocess,
                                             _pull,
                                             console,
                                             raise_exception)
        errors = executor.execute(repo_config)

        # displaying errors that occured during fetch
        for repo_name,error in errors.items():
                console_manager.add_error(repo_name,error)
        if console:
            console_manager.console()


            
    def list_branches(self,repo_name):

        repo_instance = self.get_repo(repo_name)
        absolute_path = self.get_repo_path(repo_name)
        branches = treep_git.list_branches(absolute_path)
        return branches
    

    def list_all_branches( self,
                           return_common_branches=False,
                           fetch_first=True,
                           console=True,
                           raise_exception=False ):

        if fetch_first:
            self.fetch_origin()
        
        cloned_repos =  self.get_cloned_repos()

        repo_branches = {}

        if console:
            console_manager = Console_manager()
            print(coloring.b_green("\n\tlisting branches"))

        
        for repo_name in cloned_repos:

            if console:
                print("\t\t"+coloring.cyan(repo_name)+" ... ",end='')
            
            try :
                branches = self.list_branches(repo_name)
                repo_branches[repo_name] = set(branches)
                if console:
                    print (coloring.green("OK"))
            except Exception as e:
                if console:
                    print (coloring.red("ERROR"))
                    console_manager.add_error(repo_name,str(e))
                else :
                    if raise_exception:
                        raise e

        if console or return_common_branches:
            if len(repo_branches.values())>0 :
                common_branches = list(repo_branches.values())[0].intersection(*[s for s in repo_branches.values()])
            else :
                common_branches = set()

        if len(repo_branches.values())>0 :
            all_branches = list(repo_branches.values())[0].union(*[s for s in repo_branches.values()])
        else :
            all_branches = set()
            
        if console:
            print('')
            repos = sorted(repo_branches.keys())
            for repo in repos:
                branches = repo_branches[repo]
                branches_str = [coloring.green(branch) if branch in common_branches
                                else branch for branch in branches]
                print ("\t\t"+coloring.cyan(repo)+": "+" ".join(branches_str))
            print('')

        if return_common_branches:
            return all_branches,common_branches

        return all_branches
                
            
    def get_all_existing_branches(self):

        workspace_path = self.get_workspace_path()
        if not os.path.isdir(workspace_path):
            return []
        
        return self.list_all_branches( return_common_branches=False,
                                       fetch_first=False,
                                       console=False,
                                       raise_exception=False )
            
    
    def checkout_branch(self,branch_name,
                        project_name=None,create=False,
                        console=True,raise_exception=False):

        if console:
            console_manager = Console_manager()
            print(coloring.b_green("\n\tchecking out branch "+coloring.cyan(branch_name)))

        
        if project_name is None:
            cloned_repos = self.get_cloned_repos()
        else :
            cloned_repos = self.get_repos(project_name)

        repo_paths = self.get_repos_paths(cloned_repos)

        for repo_name,path in repo_paths.items():

            if console:
                print("\t\t"+coloring.cyan(repo_name)+" ... ",end='')
            
            branches = self.list_branches(repo_name)
            if not create:
                if branch_name in branches:
                    repo_instance = self.get_repo(repo_name)
                    absolute_path = self.get_repo_path(repo_instance.name)
                    try :
                        treep_git.checkout_branch(absolute_path,branch_name,create=False)
                        if console:
                            print (coloring.green("OK"))
                    except Exception as e:
                        if console:
                            print (coloring.red("ERROR"))
                            console_manager.add_error(repo_name,str(e))
                        else:
                            if raise_exception:
                                raise e
                else :
                    print (coloring.orange("no such branch"))            
            else :
                repo_instance = self.get_repo(repo_name)
                absolute_path = self.get_repo_path(repo_instance.name)
                try :
                    treep_git.checkout_branch(absolute_path,branch_name,create=True)
                    if console:
                        print (coloring.green("OK"))
                except Exception as e:
                    if console:
                        print (coloring.red("ERROR"))
                        console_manager.add_error(repo_name,str(e))
                    else:
                        if raise_exception:
                            raise e
        if console:
            console_manager.console()
                    

    def get_status(self,repo_name,fetch_first=True,
                   console=True,raise_exception=False):

        if fetch_first:
            self.fetch_origin(repo_name=repo_name,
                              console=console,
                              raise_exception=raise_exception)

        path = self.get_repo_path(repo_name)
        status = treep_git.get_status(path)
        return status
            
                
    def get_statuses(self,fetch_first=True):

        if fetch_first:
            self.fetch_origin()
        
        r = []

        for root,dirs,files in os.walk(self._workspace_path):
            if '.git' in dirs:
                status = treep_git.get_status(root)
                if status is not None:
                    r.append(status)
        return r


    def pretty_print_workspace(self):
        
        statuses = self.get_statuses()
        status.pretty_print(statuses,self._workspace_path)

        
    def short_print_workspace(self):
        
        statuses = self.get_statuses()
        status.short_print(statuses,self._workspace_path)
        
    
    def fetch_origin( self,
                      repo_name=None,
                      console=True,
                      raise_exception=False,
                      run_multiprocess=True ):

        if console:
            console_manager = Console_manager()
            print(coloring.b_green("\n\tfetching"))

        # getting list of repos to fetch
        if repo_name is None:
            repo_names = self.get_cloned_repos()
        else :
            repo_names = [repo_name]
        repo_config = {}
        for repo_name in repo_names:
            config = {}
            config["name"]=repo_name
            instance = self.get_repo(repo_name)
            absolute_path = self.get_repo_path(repo_name)
            config["path"]=absolute_path
            repo_config[repo_name]=config

        # function for fetching a repo
        def _fetch( shared_errors,
                    shared_lock,
                    config,
                    console,
                    raise_exception,
                    nb_attempts=0):

            try :
                treep_git.fetch_origin(config["path"])
                if console:
                    with shared_lock:
                        print("\t\t"+coloring.cyan(config["name"])+" ... "+coloring.green("OK"))
            except Exception as e:
                if nb_attempts<10:
                    _fetch(shared_errors,shared_lock,config,console,raise_exception,
                           nb_attempts=nb_attempts+1)
                else :
                    if console:
                        with shared_lock:
                            print("\t\t"+coloring.cyan(config["name"])+" ... "+coloring.red("ERROR"))
                            shared_errors[config["name"]]=str(e)
                    else :
                        if raise_exception:
                            raise e

        # will execute all fetches using multiprocesses
        executor = multiprocess.Multiprocess(run_multiprocess,
                                             _fetch,
                                             console,
                                             raise_exception)
        errors = executor.execute(repo_config)

        # displaying errors that occured during fetches
        for repo_name,error in errors.items():
                console_manager.add_error(repo_name,error)
        if console:
            console_manager.console()
            
                    

    
