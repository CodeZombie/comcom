from typing import Dict
import os
import argparse
import yaml
import random

from rich.console import Console
from rich.prompt import Prompt
from rich.progress import Progress
from rich.live import Live

from comcom.comfy_ui.server.exceptions import ComfyConnectionError
from comcom.playbook.playbook import Playbook

from comcom.comcom import ComCom

class ComComCLIException(Exception):
    pass

FUN_EMOJIS = [
    'grinning_face_with_smiling_eyes', 
    'zombie', 
    'wrench', 
    'fox_face', 
    'flying_saucer', 
    'flamingo', 
    'ok_woman', 
    'ogre', 
    'muscle', 
    'mouse', 
    'fire',
    'fish',
    'watermelon',
    'maple_leaf',
    ]

class ComComCLI:
    
    def __init__(self, comcom: ComCom):
        self.console = Console()
        self.console.print("\n [b][blue]com[/][cyan]com[/][/] [bright_black]v0.1.0[/]".format(random.choice(FUN_EMOJIS)))
        self.console.print(" [bright_black]the comfyui workflow composer.[/]")
        self.console.print(" [bright_black]https://github.com/CodeZombie/comcom[/]\n")

        args = self.parse_args()

        if args.playbook_directory is not None:
            if comcom.set_root_path(args.playbook_directory):
                self.console.print("[green]Set [bold]project directory[/] to [cyan]{}[/]\n".format(os.path.abspath(args.playbook_directory)))
            else:
                raise ComComCLIException("[red]Invalid path: {}".format(os.path.abspath(args.playbook_directory)))
            
        if len(comcom.playbook_files) == 0:
            raise ComComCLIException("[red]No playbooks found in {}".format(comcom.root_path))
        
        if args.playbook is not None:
            if not comcom.set_playbook_filename(args.playbook):
                self.console.print("[red]Playbook {} not found in {}".format(args.playbook, comcom.root_path))

        if not comcom.playbook_filename and not args.no_input:
            self.console.print("[blue bold]Select a playbook:")
            for index, pb in enumerate(comcom.playbook_files):
                self.console.print("  [yellow]{}[/]:[bold]{}[/]".format(index + 1, pb))
            while comcom.playbook_filename is None:
                selected_playbook_index = input("[bold]Playbook[/] [gray](name or index)[/]: ")
                if selected_playbook_index.isnumeric() and int(selected_playbook_index) > 0 and int(selected_playbook_index) <= len(comcom.playbook_files):
                    if comcom.set_playbook_filename(comcom.playbook_files[int(selected_playbook_index) - 1]):
                        break
                else:
                    if comcom.set_playbook_filename(selected_playbook_index):
                        break
                self.console.print("[red]Invalid playbook name or index: {}".format(selected_playbook_index))

        elif not comcom.playbook_filename and args.no_input:
            raise ComComCLIException("[red]No playbook specified[/]. Please specify a playbook file by name using the [green]--playbook[/] argument")

        playbook_path = comcom.playbook_path
        if not os.path.exists(playbook_path):
            raise ComComCLIException("[red]Playbook {} not found in {}".format(comcom.playbook_filename, comcom.root_path))
        
        try:
            playbook_yaml = yaml.load(open(playbook_path), Loader=yaml.FullLoader)
        except Exception as e:
            raise ComComCLIException("[red]Failed to parse playbook yaml file:[/] {}: {}".format(comcom.playbook_filename, e))
        
        try:
            playbook = Playbook.from_dict(playbook_yaml)
        except Exception as e:
            raise ComComCLIException("[red]Error parsing playbook:[/] {}: {}".format(comcom.playbook_filename, e))

        self.console.print("[green]Set [bold]playbook[/] to [cyan]{}.yaml[/]\n".format(comcom.playbook_filename))

        workflow_name = args.workflow
        if workflow_name not in playbook.workflow_names:
            if args.no_input:
                if workflow_name is None:
                    raise ComComCLIException("[red]No workflow specified[/]. Please specify a workflow by name using the --workflow (-w) argument.")
                else:
                    raise ComComCLIException("[red]Workflow not found:[/] \"{}\"".format(workflow_name))
                
            self.console.print("Select a workflow:")
            for index, pb in enumerate(playbook.workflow_names):
                self.console.print("  [yellow]{}[/]: [bold]{}[/]".format(index + 1, pb))
            while workflow_name not in playbook.workflow_names:
                selected_workflow_value = Prompt.ask("  [bold]Workflow[/] [gray](name or index)[/]: ", default="1")
                if selected_workflow_value.isnumeric() and int(selected_workflow_value) > 0 and int(selected_workflow_value) <= len(comcom.playbook_files):
                    workflow_name = playbook.workflow_names[int(selected_workflow_value) - 1]
                    break
                elif selected_workflow_value in playbook.workflow_names:
                    workflow_name = selected_workflow_value
                    break
                self.console.print("[red]Invalid workflow name or index: {}".format(selected_workflow_value))

        self.console.print("[green]Set [bold]workflow[/] to [cyan]{}[/]".format(workflow_name))

        #on_node_progress = lambda node, value, max: self.console.print("[bold]{}[/]: [yellow]{}[/] / [yellow]{}[/]".format(node, value, max))



        self.progress = Progress()
        self.progress_task_ids: Dict = {} # node_id: task_id
        workflow = playbook.get_workflow_by_path(workflow_name)
        try:
            with Live(self.progress):
                image_outputs = comcom.comfy_server.submit_workflow_instance(workflow, self.on_node_progress)
            
        except ComfyConnectionError as e:
            raise ComComCLIException("[red][bold]ERROR: [/]{}[/]".format(str(e)))
        
        print(image_outputs)

    def on_node_progress(self, node_id, value, max):
        if node_id not in self.progress_task_ids.keys():
            self.progress_task_ids[node_id] = self.progress.add_task("Processing node [bold]#{}[/]".format(node_id), total=max)

        self.progress.update(self.progress_task_ids[node_id], completed=value)
        

    def parse_args(argv):
        parser = argparse.ArgumentParser()
        parser.add_argument('playbook_directory', default='.', nargs='?')
        parser.add_argument('--playbook', '-p', default=None, required=False)
        parser.add_argument('--workflow', '-w', default=None, required=False)
        # Add an argument to allow the user to specify whether the program should ask for input in the case of missing data, or if it should just fail.
        # By default, the program will ask for input.
        parser.add_argument('--no-input', '-n', action='store_true', default=False, required=False, help='Do not ask for input in the case of missing data. Instead, just fail.')
        return parser.parse_args()
