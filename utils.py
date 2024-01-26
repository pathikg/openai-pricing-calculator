def calculate_vision_token_cost(width, height, base_cost=85, tile_cost=170, max_size=2048, scale_size=768, tile_size=512, detail="low"):
    if detail == "low":
        return 85  # Fixed cost for low detail images
       
    # No initial resize if both dimensions are less than or equal to max_size  
    if width <= max_size and height <= max_size:  
        scaled_width = width  
        scaled_height = height  
    else:  
        # Initial resize down to fit within the max_size square  (smallest to max_size)
        if width > height:  
            scaled_height = max_size
            scaled_width = int((max_size / height) * width)  
        else:  
            scaled_width = max_size 
            scaled_height = int((max_size / width) * height)  
  
    # Scale down the shortest side to scale_size (768)  
    if scaled_width >= scale_size and scaled_height >= scale_size:  
        if scaled_width < scaled_height:  
            scaled_height = int((scale_size / scaled_width) * scaled_height)  
            scaled_width = scale_size  
        else:  
            scaled_width = int((scale_size / scaled_height) * scaled_width)  
            scaled_height = scale_size  

    # Calculate the number of 512px tiles needed  
    width_tiles = -(-scaled_width // tile_size)  # Ceiling division  
    height_tiles = -(-scaled_height // tile_size) # Ceiling division  
    total_tiles = width_tiles * height_tiles 
    
    # Calculate the total cost in tokens  
    total_cost = (tile_cost * total_tiles) + base_cost  
      
    return total_cost   