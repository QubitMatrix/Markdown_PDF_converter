# Markdown_PDF_converter
A Markdown to PDF converter built from scratch without the use of external libraries or tools and can be used to create printable markdown files.  

This tool implements a low-level Markdown-to-PDF conversion by parsing Markdown and directly generating primitive PDF drawing commands for each rendered element on a virtual canvas, avoiding external libraries. The parser interprets Markdown syntax, and for each structural component (text, headings, lists), corresponding PDF drawing operations (text positioning, font selection, line drawing) are explicitly constructed. These commands define the precise visual representation on the PDF canvas. The final PDF document is the direct concatenation of these generated low-level drawing instructions.

### Implemented Features
- Bold, Italic, BoldItalic formatting
- Headings
- Ordered lists
- Unordered lists
- Normal text
- Code statements
- Simple Blockquotes
- Horizontal break

### Future Implementation
- Code blocks
- Tables
- Images
- Links

### Pending Issues
- Add background box for code statement
- Fix content Length value and xref byte offsets
- ~Single markdown line spanning multiple lines and reaching page end~
