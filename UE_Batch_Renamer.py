import unreal

# Getting the content that is currently selected in the content browser.
def get_selected_content_browser_assets():
    editor_utility = unreal.EditorUtilityLibrary()
    selected_assets = editor_utility.get_selected_assets()
    return selected_assets

# Generating new names.
def generate_new_name_for_asset(asset):
    rename_config = {
        "prefixes_per_type": [
            {"type": unreal.MaterialInstance, "prefix": "MI_"},
            {"type": unreal.Material, "prefix": "M_"},
            {"type": unreal.Texture, "prefix": "T_"},
            {"type": unreal.NiagaraSystem, "prefix": "NS_"},
            {"type": unreal.StaticMesh, "prefix": "SM_"},
            {"type": unreal.SkeletalMesh, "prefix": "SK_"},
            {"type": unreal.Blueprint, "prefix": "BP_"},
            {"type": unreal.NiagaraEmitter, "prefix": "NE_"},
            {"type": unreal.ParticleSystem, "prefix": "PS_"}
        ]
    }
    
    name = asset.get_name()
    print(f"Asset {name} is a {type(asset)}")

    for prefix_config in rename_config["prefixes_per_type"]:
        asset_type = prefix_config["type"]
        prefix = prefix_config["prefix"]

        if isinstance(asset, asset_type):
            if not name.startswith(prefix):
                return prefix + name
            else:
                return name

    # If no matching type is found, return the original name
    return name

# Renaming the assets.
def rename_assets(assets):
    for asset in assets: 
        old_name = asset.get_name()
        old_path = asset.get_path_name()
        asset_folder = unreal.Paths.get_path(old_path)

        new_name = generate_new_name_for_asset(asset)
        new_path = asset_folder + "/" + new_name

        if new_name == old_name:
            print(f"Ignoring {old_name} as it already has the correct name")
            continue

        print(f"Renaming {old_name} to {new_name}.")

        rename_success = unreal.EditorAssetLibrary.rename_asset(old_path, new_path)
        if not rename_success:
            unreal.log_error("Could not rename: " + old_path)

# Iterating over the array of currently selected content.
def run():
    current_assets = get_selected_content_browser_assets()
    rename_assets(current_assets)

run()