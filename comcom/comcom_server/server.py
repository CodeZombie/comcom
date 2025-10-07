from typing import List, Dict
from nicegui import ui, app
from comcom.comcom import ComCom, Recipe
from comcom.comfy_ui.file_management.media_metadata import MediaMetadata
import asyncio
from PIL import Image
import base64
from io import BytesIO
from starlette import responses
import yaml
import time

# MODFILES
# modfiles are normal yaml files that contain overrides for any recipe.
# They dont contain any special syntax.
# nodes:
#   path.to.node:
#       Some Node.slot: value
# You load them into the UI with a separate selecter underneath the recipe file selector
# 

def pil_image_to_base64(pil_image: Image):
    buffered = BytesIO()
    pil_image.save(buffered, format="PNG")
    buffered.seek(0)
    base64_encoded_bytes = base64.b64encode(buffered.read())
    return 'data:image/png;base64,' + base64_encoded_bytes.decode('ascii')

# def safe_load_deepyaml(filepath):
#     with open(filepath, 'r') as file:
#         lines = file.readlines()
#         if len(lines) <= 1:
#             return None
#         yaml_content = "".join(lines[1:])
#         data = yaml.safe_load(yaml_content)
#         return data

# def update_mod_file(root_recipe_name: str, recipe_path: str, node_proprerty_path: str | list, value=None) -> str:
#     data = {}
#     if root_recipe_name.endswith('.ccmod'):
#         data = safe_load_deepyaml(f"{root_recipe_name}.yaml")
    
#     split_recipe_path = recipe_path.split('.')
#     if len(split_recipe_path) == 1:
        

    
@ui.page('/file')
def get_file(filename: str):
    return responses.FileResponse(filename)

@ui.page('/')
def index():
    final_image_table = None
    async def execute_recipe(recipe) -> int:
        app.storage.client['is_executing'] = True
        await asyncio.to_thread(comcom.execute_recipe, recipe, on_execute_progress, on_preview_image)
        app.storage.client['is_executing'] = False
        thumbnail_row.refresh()
        progress_bar.value = 0

    def interrupt():
        comcom.interrupt()
        progress_bar.value = 0
        app.storage.client['is_executing'] = False

    def on_preview_image(image: Image):
        preview_image.set_source(pil_image_to_base64(image))

    def on_execute_progress(*args, **kwargs):
        progress_bar.value = args[1] / args[2]

    def refresh():
        old_selected_recipe_global_ids = app.storage.client.get('selected_recipe_global_ids', [])
        comcom = ComCom()
        comcom.select_recipe_file(app.storage.client.get('selected_recipe_file_name'))
        app.storage.client['selected_recipe_global_ids'] = old_selected_recipe_global_ids
        
        recipe_file_selector.refresh()
        recipe_tree.refresh()
        recipe_details.refresh()

        #self.comcom = ComCom()
        #selected_recipe_global_ids = [r.global_id for r in self.selected_recipes]
        #self.select_recipe_file(self.selected_recipe_file)
        #self.select_recipes(selected_recipe_global_ids)
        #self.
        #self.recipe_tree.refresh()
        #self.recipe_details.refresh()

    def recipe_to_ui_list(recipe: Recipe):
        if not recipe:
            return []
        
        new_ui_element = {
            'id': recipe.global_id,
            'label': str(recipe.id), 
            'children': []
        }
        for r in recipe.recipes.values():
            new_ui_element['children'].extend(recipe_to_ui_list(r))

        return [new_ui_element]

    @ui.refreshable
    def thumbnail_row():
        def set_primary_generated_image(name: str, media_metadata: MediaMetadata | str):
            if final_image_table:
                final_image_table.rows = []

            if isinstance(media_metadata, str):
                final_image.source = media_metadata
            else:
                final_image.source = f"/file?filename={media_metadata.local_path.path_str}&t={time.time()}" #pil_image_to_base64(Image.open(media_metadata.local_path.path_str))
                new_rows = [
                    {'property': 'name', 'value': media_metadata.local_path.name},
                    {'property': 'stored sha1', 'value': media_metadata.sha1},
                    {'property': 'file sha1', 'value': media_metadata.local_path.sha1},
                    {'property': 'requires editing', 'value': media_metadata.local_path.requires_editing},
                ]
                if media_metadata.local_path.requires_editing:
                    new_rows.append({'property': 'has been edited', 'value': media_metadata.local_file_needs_to_be_edited_but_hasnt_been_edited_yet})
                if final_image_table:
                    final_image_table.add_rows(new_rows)
                    final_image_table.update()

        selected_recipes = []
        for recipe_global_id in app.storage.client.get('selected_recipe_global_ids', []):
            found_recipe = comcom.get_recipe(recipe_global_id)
            if found_recipe:
                selected_recipes.append(found_recipe)

        all_media_metadata = {}
        for recipe in selected_recipes:
            for name, meta in recipe.saved_media_metadata.items():
                if not meta:
                    continue
                all_media_metadata[f"{recipe.global_id}.{name}"] = meta
        
        with ui.row().classes('flex-nowrap overflow-x-auto gap-4 p-2'):
            for key, value in all_media_metadata.items():
                ui.image(f"/file?filename={value.local_path.path_str}&t={time.time()}").classes('w-24 h-24 object-cover rounded-md shadow-md cursor-pointer transition-transform hover:scale-105') \
                    .on('click', lambda key=key, value=value: set_primary_generated_image(key, value))
                
        if len(all_media_metadata) > 0:
            set_primary_generated_image(list(all_media_metadata.keys())[0], list(all_media_metadata.values())[0])
        else:
            set_primary_generated_image("None", "https://cdn-icons-png.flaticon.com/512/5978/5978100.png")

    @ui.refreshable
    def recipe_tree():
        def select_recipes(recipe_global_ids):
            app.storage.client['selected_recipe_global_ids'] = recipe_global_ids
            recipe_details.refresh()
            thumbnail_row.refresh()

        recipe_name = app.storage.client.get('selected_recipe_file_name', None)
        if recipe_name:
            if not comcom.select_recipe_file(recipe_name):
                ui.dialog(f"Failed to select recipe {recipe_name}")

            ui.tree(
                recipe_to_ui_list(comcom.selected_recipe), 
                tick_strategy='strict') \
            .expand() \
            .on_tick(lambda e: select_recipes(e.value)) \
            .tick(app.storage.client.get('selected_recipe_global_ids', []))

    @ui.refreshable
    def recipe_file_selector():
        def select_recipe_name(name):
            app.storage.client['selected_recipe_file_name'] = name
            app.storage.client['selected_recipe_global_ids'] = []
            recipe_details.refresh()
            recipe_tree.refresh()
            thumbnail_row.refresh()

        file_options = {file: file for file in comcom.recipe_files}
        ui.select(
            options=file_options, 
            value=app.storage.client.get('selected_recipe_file_name', None),
            label='Recipe File', 
            on_change=lambda e: select_recipe_name(e.value)
        ).classes('w-full')

    def create_element_from_param(param_path, param_value, recipe: Recipe) -> None:
        def update_param(param_path_, new_value_, recipe_: Recipe):
            print(f"Updating recipe node {param_path_} to {new_value_}")
            if isinstance(param_path_, List):
                recipe_.nodes[f"{param_path_[0]}.{param_path_[1]}"] = new_value_
                return
            recipe_.nodes[param_path_] = new_value_

        def pretty_param_path(param_path_):
            if isinstance(param_path_, List):
                return '.'.join(param_path_)
            return param_path_
        
        if isinstance(param_value, str):
            ui.textarea(
                pretty_param_path(param_path), 
                value=param_value,
                on_change=lambda e: update_param(param_path, str(e.value), recipe)
                ).classes('w-full').props('autogrow')
        if isinstance(param_value, int):
            ui.number(
                pretty_param_path(param_path), 
                value=param_value,
                on_change=lambda e: update_param(param_path, int(e.value), recipe)
                ).classes('w-full')
            
        if isinstance(param_value, float):
            ui.number(
                pretty_param_path(param_path), 
                value=param_value, 
                precision=3,
                on_change=lambda e: update_param(param_path, float(e.value), recipe)
                ).classes('w-full')
        if isinstance(param_value, list):
            ui.textarea(pretty_param_path(param_path), value='\n'.join(param_value)).classes('w-full').props('autogrow').disable()

        if isinstance(param_value, dict):
            for k, v in param_value.items():
                print([param_path, k])
                create_element_from_param([param_path, k], v, recipe)

    @ui.refreshable
    def recipe_details():
        selected_recipe_paths = app.storage.client.get('selected_recipe_global_ids', [])

        recipes: List[Recipe] = []
        for recipe_path in selected_recipe_paths:
            recipes.append(comcom.get_recipe(recipe_path))

        for selected_recipe in recipes:
            with ui.card().classes('w-full'):
                ui.label(selected_recipe.global_id)
                ui.label(selected_recipe.workflow)
                for node_name, params in (selected_recipe.nodes | selected_recipe.load | selected_recipe.save).items():
                    if isinstance(params, dict):
                        with ui.expansion(node_name).classes('w-full'):
                            for param_name, param_value in params.items():
                                create_element_from_param([node_name, param_name], param_value, selected_recipe)
                    else:
                        create_element_from_param(node_name, params, selected_recipe)

                with ui.row().classes('w-full'):
                    ui.space()
                    ui.button("Save API Graph", on_click=lambda: ui.download.content(comcom.comfy_server.get_preview_of_resolved_api_graph(selected_recipe), f"resolved_{selected_recipe.id}.json"))
                    ui.button("Execute", on_click=lambda: execute_recipe(selected_recipe)) \
                    .bind_enabled_from(app.storage.client, 'is_executing', backward=lambda v: not v)

    comcom = ComCom()
    

    ui.page_title("ComCom")
    with ui.header().classes('items-center justify-between'):
        ui.label('ComCom Recipe Executor').classes('text-xl')
        ui.space()
        progress_bar = ui.linear_progress(color='warning').classes('w-1/4').bind_value_from(app.storage.client, 'execution_progress')
        ui.button("Halt").props('color=red').on_click(interrupt).bind_enabled_from(app.storage.client, 'is_executing')
        ui.button("Refresh").on_click(refresh)

    #with ui.element('div').classes('w-full h-[500px] columns-1 md:columns-3'):
    with ui.row().classes('w-full mx-auto grid grid-cols-1 md:grid-cols-12'):
        with ui.column().classes('col-span-12 md:col-span-3'):
            with ui.card().props('flat bordered').classes('w-full'):
                recipe_file_selector()
                ui.label("Nothing Selected").bind_text_from(app.storage.client, 'selected_recipe_file_name', lambda v: f'Selected: {v}')
                recipe_tree()
        with ui.column().classes('col-span-12 md:col-span-5'):
            with ui.card().props('flat bordered').classes('w-full'):
                with ui.tabs().classes('w-full h-full') as tabs:
                    latent_preview_tab = ui.tab('Preview')
                    finished_images_tab = ui.tab('Generated Images')
                with ui.tab_panels(tabs, value=latent_preview_tab).classes('w-full h-full').style('background: 0;'):
                        with ui.tab_panel(latent_preview_tab).classes('w-full items-center justify-center'):
                            IMAGE_URL = "https://i.pinimg.com/736x/95/47/0c/95470c8d65cb8bc6801814bbdf76f98b.jpg"
                            preview_image = ui.image(IMAGE_URL).classes('w-[500px] h-auto max-w-full max-h-full shadow-xl')
                        with ui.tab_panel(finished_images_tab).classes('w-full items-center justify-center'):
                            IMAGE_URL = "https://fastly.picsum.photos/id/684/640/360.jpg?hmac=XI9EvJ5cgD5EOo18eNf8BT62dp9CIb42ifOw1G5D-R0"
                            with ui.row():
                                final_image = ui.image(IMAGE_URL).classes('w-[500px] h-auto max-w-full max-h-full shadow-xl')
                            with ui.row():
                                ui.space()
                                thumbnail_row()
                            with ui.row():
                                final_image_table = ui.table(columns=[
                                    {'name': 'property', 'label': "Property", 'field': 'property', 'align': 'left'},
                                    {'name': 'value', 'label': 'Value', 'field': 'value', 'align': 'right'}
                                    ],
                                    rows=[],
                                    ).classes('w-full')
                    
        with ui.column().classes('col-span-12 md:col-span-4'):
            with ui.card().props('flat bordered').classes('w-full'):
                recipe_details()

def start_server():
    ui.run(dark=True)
