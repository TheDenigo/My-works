import binascii

def decode_sav_file(filepath, max_blocks=100):
    try:
        with open(filepath, 'rb') as file:
            data = file.read()

        print("--------------------------------------------")
        print("      Decoded Data (Grouped Analysis)")
        print("--------------------------------------------")

        marker_byte = b'\xab'
        marker_positions = []
        for i, byte in enumerate(data):
            if byte == marker_byte[0]:
                marker_positions.append(i)

        blocks = []
        start = 0
        for end in marker_positions:
            block = data[start:end]
            blocks.append(block)
            start = end

        if start < len(data):
            blocks.append(data[start:])


        grouped_blocks = []
        current_group = []
        block_count = 0
        for i, block in enumerate(blocks):
            if block_count >= max_blocks:
                break

            block_type = "Unknown"
            first_two_bytes = ""
            if len(block) > 1:
                first_two_bytes = binascii.hexlify(block[:2]).decode('utf-8')

            if first_two_bytes == "abaa" or first_two_bytes == "abba":
                if current_group:
                    grouped_blocks.append(current_group)
                    current_group = []

                current_group.append((i, block, "Type A"))
                block_count +=1
            else:
                 current_group.append((i, block, block_type))
                 block_count += 1

            if i == len(blocks) - 1:
               grouped_blocks.append(current_group)




        for group in grouped_blocks:
            print("-------------------")
            for i, block, block_type in group:
               block_type = "Unknown"
               first_two_bytes = ""

               if len(block) > 1:
                 first_two_bytes = binascii.hexlify(block[:2]).decode('utf-8')


               if first_two_bytes == "abaa" or first_two_bytes == "abba":
                   block_type = "Type A (Marker/Header)"
               elif first_two_bytes == "abee":
                   block_type = "Type B (Data)"
               elif first_two_bytes == "abea":
                   block_type = "Type C (Coords)"
               elif first_two_bytes == "ab5d":
                   block_type = "Type D (Flags)"
               elif first_two_bytes == "abdd":
                   block_type = "Type E"
               elif first_two_bytes == "ab9e":
                    block_type = "Type F"
               elif first_two_bytes == "ab2d":
                   block_type = "Type G"
               elif first_two_bytes == "abae":
                   block_type = "Type H"
               elif first_two_bytes == "ab12":
                    block_type = "Type I"
               elif first_two_bytes == "ab49":
                    block_type = "Type J"
               elif first_two_bytes == "ab0d":
                   block_type = "Type K"
               elif first_two_bytes == "ab95":
                 block_type = "Type L"
               elif first_two_bytes == "abaf":
                 block_type = "Type M"
               elif first_two_bytes == "ab1d":
                 block_type = "Type N"



               print(f"Block {i} (length {len(block)}): Type: {block_type}")
               print(f"  Hex: {binascii.hexlify(block).decode('utf-8')}")

    except FileNotFoundError:
        print(f"Error: File not found: {filepath}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    sav_file_path = input("Enter the path to your .sav file: ")
    decode_sav_file(sav_file_path, max_blocks=100)