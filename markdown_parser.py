import re
import sys

# Format text for bold, italic, etc and handle multiline sentences
def format_text(txt,coord,indent):
    txt = txt.replace("(","\(").replace(")","\)")
    num_lines = 1
    total_chars = 90
    indent_chars = 3 * indent
    available_chars = total_chars - indent_chars # Handle moving cursor to next line

    # Regex patterns
    bold_italic_p1 = r"\*\*\*(.*?)\*\*\*"
    bold_italic_p2 = r"___(.*?)___"
    bold_p1 = r"\*\*(.*?)\*\*"
    bold_p2 = r"__(.*?)__"
    italic_p1 = r"\*\S(.*?)\*"
    italic_p2 = r"_\S(.*?)_"
    code_p = r"`(.*?)`"
    pattern = re.compile("|".join([bold_italic_p1,bold_italic_p2,bold_p1,bold_p2,italic_p1,italic_p2,code_p]))

    matches = re.finditer(pattern,txt)
    bold_italic_pos = []
    bold_pos = []
    italic_pos = []
    code_pos = []
    pdf_txt = ""

    # Iterate matches using Regex Grouping and categorise into their categories
    for match in matches:
        start_pos = match.start()
        # Bold_Italic text
        if(match.group(1) or match.group(2)):
            word = match.group(1) or match.group(2)
            end_pos = start_pos + 3 +len(word) + 3
            bold_italic_pos.append([start_pos,end_pos])
        
        # Bold text
        elif(match.group(3) or match.group(4)):
            word = match.group(3) or match.group(4)
            end_pos = start_pos + 2 + len(word) + 2
            bold_pos.append([start_pos,end_pos])

        # Italic text
        elif(match.group(5) or match.group(6)):
            word = match.group(5) or match.group(6)
            end_pos = start_pos +1 +len(word)+2
            italic_pos.append([start_pos,end_pos])

        # Code blocks
        elif(match.group(7)):
            word = match.group(7)
            end_pos = start_pos + 1 +len(word) + 1
            code_pos.append([start_pos,end_pos])
    
    # Generate raw pdf for the text
    pos = 0
    bold = 0
    italic = 0
    bold_italic = 0
    code = 0
    normal_txt = ""
    bold_txt = ""
    italic_txt = ""
    bold_italic_txt = ""
    code_txt = ""
    #x_coord = coord[0] - 3
    #y_coord = coord[1] - 5
    written_txt = 0 # For codeblock background - FUTURE FEATURE

    # Iterate text and format and form raw pdf statements
    while(pos < len(txt)):
        bold = 0
        italic = 0
        bold_italic = 0
        code = 0

        # Handle bold words and normal text till that word
        for start_pos, end_pos in bold_pos:
            if(pos == start_pos):
                bold_txt = txt[start_pos+2:end_pos-2]
                pos = end_pos - 1
                bold = 1

                # Handle normal text before reaching bold text
                while(True):
                    # If exceeds line limit split into multiple lines
                    if(available_chars < len(normal_txt)):
                        # Find last complete word to fit in line and move cursor to next line
                        try:
                            end_index = available_chars - normal_txt[:available_chars][::-1].index(' ') - 1
                            pdf_txt += f"/F1 12 Tf\n({normal_txt[:end_index]}) Tj\n1 0 0 1 {coord[0]} {coord[1] - 15} Tm\n"
                        except:
                            pdf_txt += f"1 0 0 1 {coord[0]} {coord[1] - 15} Tm\n"
                            end_index = 0

                        # Split the remaining of the text to write in next lines
                        normal_txt = normal_txt[end_index:].strip()
                        coord[1] -= 15
                        num_lines += 1
                        written_txt = 0
                        available_chars = total_chars - indent_chars 
                    
                    # Fill the remaining text in line and break out
                    else:
                        pdf_txt += f"/F1 12 Tf\n({normal_txt}) Tj\n"
                        written_txt += len(normal_txt)
                        available_chars -= len(normal_txt)
                        break

                # Handle bold text
                while(True):
                    if(available_chars < len(bold_txt)):
                        try:
                            end_index = available_chars - bold_txt[:available_chars][::-1].index(' ') - 1
                            pdf_txt += f"/F2 12 Tf\n({bold_txt[:end_index]}) Tj\n1 0 0 1 {coord[0]} {coord[1] - 15} Tm\n"
                        except:
                            pdf_txt += f"1 0 0 1 {coord[0]} {coord[1] - 15} Tm\n"
                            end_index = 0

                        bold_txt = bold_txt[end_index:].strip()
                        coord[1] -= 15
                        num_lines += 1
                        written_txt = 0
                        available_chars = total_chars - indent_chars
                    else:
                        pdf_txt += f"/F2 12 Tf\n({bold_txt}) Tj\n"
                        written_txt += len(bold_txt)
                        available_chars -= len(bold_txt)
                        break
                    
                normal_txt = ""
                break

            # If pos not found break optimally
            elif(pos < start_pos):
                break
        
        # Handle italic words and normal text till that word
        for start_pos, end_pos in italic_pos:
            if(pos == start_pos):
                italic_txt = txt[start_pos+1:end_pos-1]
                pos = end_pos - 1
                italic = 1

                # Handle normal words before the italic words
                while(True):
                    if(available_chars < len(normal_txt)):
                        try:
                            end_index = available_chars - normal_txt[:available_chars][::-1].index(' ') - 1
                            pdf_txt += f"/F1 12 Tf\n({normal_txt[:end_index]}) Tj\n1 0 0 1 {coord[0]} {coord[1] - 15} Tm\n"
                        except:
                            pdf_txt += f"1 0 0 1 {coord[0]} {coord[1] - 15} Tm\n"
                            end_index = 0
                        normal_txt = normal_txt[end_index:].strip()
                        coord[1] -= 15
                        num_lines += 1
                        written_txt = 0
                        available_chars = total_chars - indent_chars
                    else:
                        pdf_txt += f"/F1 12 Tf\n({normal_txt}) Tj\n"
                        written_txt += len(normal_txt)
                        available_chars -= len(normal_txt)
                        break

                # Handle italic words
                while(True):
                    if(available_chars < len(italic_txt)):
                        try:
                            end_index = available_chars - italic_txt[:available_chars][::-1].index(' ') - 1
                            pdf_txt += f"/F3 12 Tf\n({italic_txt[:end_index]}) Tj\n1 0 0 1 {coord[0]} {coord[1] - 15} Tm\n"
                        except:
                            pdf_txt += f"1 0 0 1 {coord[0]} {coord[1] - 15} Tm\n"
                            end_index = 0
                        italic_txt =italic_txt[end_index:].strip()
                        coord[1] -= 15
                        num_lines += 1
                        written_txt = 0
                        available_chars = total_chars - indent_chars
                    else:
                        pdf_txt += f"/F3 12 Tf\n({italic_txt}) Tj\n"
                        written_txt += len(italic_txt)
                        available_chars -= len(italic_txt)
                        break

                normal_txt = ""
                break
            if(pos < start_pos):
                break
       
        # Handle bold_italic words and normal words till it
        for start_pos, end_pos in bold_italic_pos:
            if(pos == start_pos):
                bold_italic_txt = txt[start_pos+3:end_pos-3]
                pos = end_pos - 1
                bold_italic = 1

                # Handle normal words before bold_italic words
                while(True):
                    if(available_chars < len(normal_txt)):
                        try:
                            end_index = available_chars - normal_txt[:available_chars][::-1].index(' ') - 1
                            pdf_txt += f"/F1 12 Tf\n({normal_txt[:end_index]}) Tj\n1 0 0 1 {coord[0]} {coord[1] - 15} Tm\n"
                        except:
                            pdf_txt += f"1 0 0 1 {coord[0]} {coord[1] - 15} Tm\n"
                            end_index = 0
                        normal_txt =normal_txt[end_index:].strip()
                        coord[1] -= 15
                        num_lines += 1
                        written_txt = 0
                        available_chars = total_chars - indent_chars
                    else:
                        pdf_txt += f"/F1 12 Tf\n({normal_txt}) Tj\n"
                        written_txt += len(normal_txt)
                        available_chars -= len(normal_txt)
                        break

                # Handle bold_italic words
                while(True):
                    if(available_chars < len(bold_italic_txt)):
                        try:
                            end_index = available_chars - bold_italic_txt[:available_chars][::-1].index(' ') - 1
                            pdf_txt += f"/F4 12 Tf\n({bold_italic_txt[:end_index]}) Tj\n1 0 0 1 {coord[0]} {coord[1] - 15} Tm\n"
                        except:
                            pdf_txt += f"1 0 0 1 {coord[0]} {coord[1] - 15} Tm\n"
                            end_index = 0
                        bold_italic_txt = bold_italic_txt[end_index:].strip()
                        coord[1] -= 15
                        num_lines += 1
                        written_txt = 0
                        available_chars = total_chars - indent_chars
                    else:
                        pdf_txt += f"/F4 12 Tf\n({bold_italic_txt}) Tj\n"
                        written_txt += len(bold_italic_txt)
                        available_chars -= len(bold_italic_txt)
                        break

                normal_txt = ""
                break
            if(pos < start_pos):
                break

        # Handle code words and normal words till it
        for start_pos, end_pos in code_pos:
            if(pos == start_pos):
                code_txt = txt[start_pos+1:end_pos-1]
                pos = end_pos - 1
                code = 1
                height = 15

                # Handle normal words before code
                while(True):
                    if(available_chars < len(normal_txt)):
                        try:
                            end_index = available_chars - normal_txt[:available_chars][::-1].index(' ') - 1
                            pdf_txt += f"/F1 12 Tf\n({normal_txt[:end_index]}) Tj\n1 0 0 1 {coord[0]} {coord[1] - 15} Tm\n"
                        except:
                            pdf_txt += f"1 0 0 1 {coord[0]} {coord[1] - 15} Tm\n"
                            end_index = 0
                        normal_txt =normal_txt[end_index:].strip()
                        coord[1] -= 15
                        num_lines += 1
                        written_txt = 0
                        available_chars = total_chars - indent_chars
                    else:
                        pdf_txt += f"/F1 12 Tf\n({normal_txt}) Tj\n"
                        written_txt += len(normal_txt)
                        available_chars -= len(normal_txt)
                        break
                
                # Handle code words
                while(True):
                    if(available_chars < len(code_txt)):
                        try:
                            end_index = available_chars - code_txt[:available_chars][::-1].index(' ') - 1
                            width = 6.3 * end_index # Background box - FUTURE FEATURE
                            x_shift = written_txt * 5.4 # Background box - FUTURE FEATURE
                            pdf_txt += f"0.3 0.6 0.8 rg\n/F5 10 Tf\n({code_txt[:end_index]}) Tj\n0 0 0 rg\n1 0 0 1 {coord[0]} {coord[1] - 15} Tm\n"
                        except:
                            pdf_txt += f"1 0 0 1 {coord[0]} {coord[1] - 15} Tm\n"
                            end_index = 0
                        code_txt =code_txt[end_index:].strip()
                        coord[1] -= 15
                        num_lines += 1
                        written_txt = 0
                        available_chars = total_chars - indent_chars
                    else:
                        width = 6.3 *len(code_txt) # Background box - FUTURE FEATURE
                        x_coord = coord[0] - 3 # Background box - FUTURE FEATURE
                        y_coord = coord[1] - 5 # Background box - FUTURE FEATURE
                        pdf_txt += f"0.3 0.6 0.8 rg\n/F5 10 Tf\n({code_txt}) Tj\n0 0 0 rg\n"
                        available_chars -= len(code_txt)
                        break

                normal_txt = ""
                break
            if(pos < start_pos):
                break
        
        # Store normal words
        if(not bold and not italic and not bold_italic and not code):
            normal_txt += txt[pos]
        pos += 1

    # Handle last set of normal words
    if(not bold and not italic and not bold_italic and not code):
        while(True):
            if(available_chars < len(normal_txt)):
                try:
                    end_index = available_chars - normal_txt[:available_chars][::-1].index(' ') - 1
                    pdf_txt += f"/F1 12 Tf\n({normal_txt[:end_index]}) Tj\n1 0 0 1 {coord[0]} {coord[1] - 15} Tm\n"
                except:
                    pdf_txt += f"1 0 0 1 {coord[0]} {coord[1] - 15} Tm\n"
                    end_index = 0
                normal_txt = normal_txt[end_index:].strip()
                coord[1] -= 15
                num_lines += 1
                written_txt = 0
                available_chars = total_chars - indent_chars
            else:
                pdf_txt += f"/F1 12 Tf\n({normal_txt}) Tj\n"
                written_txt += len(normal_txt)
                available_chars -= len(normal_txt)
                break

    return pdf_txt,num_lines

# Handle headings 1 - 6
def headings(line,coord,flags):
    heading = line[line.index(' ')+1:].strip()
    heading_num = line.count('#')
    fontsize = 10 + 2*(7-heading_num)
    pdf_line = f"/F2 {fontsize} Tf\n1 0 0 1 {coord[0]} {coord[1]} Tm\n({heading}) Tj\n"
    coord[1] -= (15 + [3,5,7,9,11,13][6-heading_num]) #*(7-heading_num))
    flags['add_yspace'] = 0 # Avoid leaving extra space before next line
    return pdf_line

# Handle unordered lists
def unordered_lists(line,coord,flags):
    indent = line.count("\t")
    txt = line[line.index(' ')+1:].strip()

    fill = 's' if indent%2 else 'f' # Set bullet point fill option

    # Set text coordinates
    coord[1] = coord[1] if(indent or not flags['add_yspace']) else coord[1] - 10
    y_coord = coord[1]
    coord[0] += (indent+1)*20
    x_coord = coord[0]

    # Format text content
    txt,num_lines = format_text(txt,coord,indent)
    coord[0] -= (indent+1)*20

    # Circle bullet point
    if(indent < 2):
        # Set bullet coordinates
        bul_x = x_coord - 5
        bul_y = y_coord + 3
        line_bullet = f"0 0 0 rg\n{bul_x} {bul_y} m\n{bul_x} {bul_y+2}  {bul_x-3} {bul_y+2}  {bul_x-3} {bul_y} c\n{bul_x-3} {bul_y-2}  {bul_x} {bul_y-2}  {bul_x} {bul_y} c\n{fill}\n"

    # Square bullet point
    else:
        bul_x = x_coord - 8
        bul_y = y_coord + 3
        width = height = 3
        line_bullet = f"0 0 0 rg\n{bul_x} {bul_y} {width} {height} re\n{fill}\n"
    
    coord[1] -= 15
    line_txt = f"/F1 12 Tf\n1 0 0 1 {x_coord} {y_coord} Tm\n{txt}\n"
    pdf_line = line_bullet + line_txt
    flags['add_yspace'] = 1 # Add extra line space before next line
    return pdf_line
 
# Handle ordered lists
def ordered_lists(line, coord,flags):
    line_stripped = line.strip()
    indent = line.count('\t')
    num = int(line_stripped[:line_stripped.index('.')])
    txt = line_stripped[line_stripped.index('.')+2:]

    # Set text coordinates
    coord[0] = coord[0] + 10 + (indent*20) + 21
    coord[1] = coord[1] if(num != 1 or indent or not flags['add_yspace']) else coord[1] - 10
    x_coord = coord[0] - 21
    y_coord = coord[1]

    # Format text
    txt,num_lines = format_text(txt,coord,indent)

    pdf_line = f"/F1 12 Tf\n1 0 0 1 {x_coord} {y_coord} Tm\n({num}. ) Tj\n1 0 0 1 {coord[0]} {y_coord} Tm\n{txt}\n"
    coord[0] = coord[0] - 10 - (indent*20) - 21
    coord[1] -= 15
    flags['add_yspace'] = 1
    return pdf_line

# Handle normal text
def normal_txt(line, coord,flags):
    # Set text coordinates
    x_coord = coord[0]
    coord[1] = coord[1] if(not flags['add_yspace']) else coord[1] - 10
    y_coord = coord[1]

    txt = line.strip()
    txt,num_lines = format_text(txt,coord,0)

    pdf_line = f"/F1 12 Tf\n1 0 0 1 {x_coord} {y_coord} Tm\n{txt}\n"
    coord[1] -= 15
    flags['add_yspace'] = 0
    return pdf_line

# Handle blockquote content
def blockquote(line, coord, flags):
    txt = line.strip()[2:]

    # Set coordinates
    box_x = coord[0]
    y_coord = coord[1]
    coord[0] += 20

    # Format text
    txt,num_lines = format_text(txt,coord,1)

    height = 20 + 15*(num_lines)
    box_y = y_coord - height + 20
    width = 490
    pdf_line = f"0.9 0.9 0.9 rg\n{box_x} {box_y} {width} {height} re\nf\n0.7 0.7 0.7 rg\n{box_x} {box_y} 5 {height} re\nf\n0 0 0 rg\n/F1 12 Tf\n1 0 0 1 {coord[0]} {y_coord} Tm\n{txt}\n"

    coord[0] -= 20
    coord[1] -=30
    return pdf_line

# Add next pdf page
def add_page(page_obj_id):
    pdf_page = f"{page_obj_id} 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Contents {page_obj_id+1} 0 R /Resources << /Font << /F1 3 0 R /F2 4 0 R /F3 5 0 R /F4 6 0 R /F5 7 0 R >> >> >>\nendobj\n"
    return pdf_page

def markdown_pdf(filename):
    with open(filename,"r") as f:
        lines = f.readlines()

    # Set printable edges
    coord = [50, 770] #x,y

    flags = {'add_yspace':0, 'add_newline':1}

    # Metadata
    page_count = 1
    page_ids = "8 0 R"
    page_obj_id = 8
    pdf_content = ""
    pdf_contents_obj = ""
    pdf_pages = add_page(page_obj_id)
    page_obj_id += 2

    # Iterate each line of markdown
    for line in lines:
        print(line)
        heading_regex = "^#+ *"
        unorderedlist_regex = "^- *"
        orderedlist_regex = "^\d\. *"
        estimated_num_lines = len(line) // 80 
        # If y coordinate is less add new page
        if((coord[1] - 15 * estimated_num_lines) < 100):
            content_length = len(pdf_content) # TO BE FIXED
            pdf_contents_obj += f"{page_obj_id-1} 0 obj\n<< /Length {content_length} >>\nstream\nBT\nq\n{pdf_content}\nQ\nET\nendstream\nendobj\n"
            pdf_content = ""

            # Set values for next page
            coord = [50,770]
            page_ids += f" {page_obj_id} 0 R"
            pdf_pages += add_page(page_obj_id)
            page_obj_id += 2
            page_count += 1

        # Newline
        if(line and not len(line.strip()) and flags['add_newline']):
            coord[1] -= 30
            flags['add_newline'] = 0
       
        # Horizontal break
        elif(line.strip() == '---' or line.strip() == '***' or line.strip() == '___'):
            pdf_content += f"{coord[0]} {coord[1]} {490} {2} re\nf\n"
        
        # Headings
        elif(re.search(heading_regex,line)):
            flags['add_newline'] = 1
            pdf_content += headings(line,coord,flags)
        
        # Unordereed lists
        elif(re.search(unorderedlist_regex,line.strip())):
            flags['add_newline'] = 1
            pdf_content += unordered_lists(line,coord,flags)

        # Ordered lists
        elif(re.search(orderedlist_regex, line.strip())):
            flags['add_newline'] = 1
            pdf_content += ordered_lists(line, coord, flags)

        # Blockquotes
        elif(len(line.strip())>0 and line.strip()[0] == '>'):
            pdf_content += blockquote(line, coord, flags)

        # Normal text
        else:
            flags['add_newline'] = 1
            pdf_content += normal_txt(line,coord,flags)


    # Raw pdf statements for last page contents
    content_length = len(pdf_content) # TO BE FIXED
    pdf_contents_obj += f"{page_obj_id-1} 0 obj\n<< /Length {content_length} >>\nstream\nBT\nq\n{pdf_content}\nQ\nET\nendstream\nendobj\n"

    # Form the pdf header and trailer
    pdf_header = f"%PDF-1.4\n1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n2 0 obj\n<< /Type /Pages /Kids [{page_ids}] /Count {page_count} >>\nendobj\n3 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Times-Roman >>\nendobj\n4 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Times-Bold >>\nendobj\n5 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Times-Italic >>\nendobj\n6 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Times-BoldItalic >>\nendobj\n7 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Courier-Bold >>\nendobj\n"

    pdf_trailer = f"xref\n0 9 % No of objects +1\n0000000000 65535 f % first object is always free\n0000000010 00000 n % in use\n0000000053 00000 n\n0000000101 00000 n\n0000000230 00000 n\n0000000331 00000 n\n0000000412 00000 n\ntrailer\n<< /Size 9 /Root 1 0 R >> % 9 - no.objcets\nstartxref\n474\n%%EOF" # TO BE FIXED

    # Combine all parts of the Raw PDF and write into a PDF file
    pdf_str = f"{pdf_header}\n{pdf_pages}\n{pdf_contents_obj}\n{pdf_trailer}"
    pdf = f"{filename.split('.')[0]}.pdf"
    pdf_file = open(pdf,"w")
    print(pdf_str, file=pdf_file)
    pdf_file.close()


# Main callpoint
if __name__ == "__main__":
    markdown_pdf(sys.argv[1])
