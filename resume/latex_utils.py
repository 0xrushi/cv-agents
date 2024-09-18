import json
import subprocess
import os

def render_latex_to_pdf(tex_file_path, output_dir):
    """
    Renders a LaTeX file to PDF using pdflatex.

    Args:
    tex_file_path (str): The path to the LaTeX file.
    output_dir (str): The directory where the output PDF will be saved.

    Returns:
    str: The path to the generated PDF file, or None if an error occurred.
    """
    try:
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)

        # Get the base name of the tex file (without extension)
        base_name = os.path.splitext(os.path.basename(tex_file_path))[0]
        
        # Run pdflatex twice to ensure all references are resolved
        for _ in range(2):
            subprocess.run([
                'pdflatex',
                '-output-directory', output_dir,
                tex_file_path
            ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            subprocess.run([
                'pdflatex',
                '-output-directory', output_dir,
                tex_file_path
            ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            # Delete auxiliary files (e.g., .aux, .log, .out)
            aux_files = ['.aux', '.log', '.out']
            for ext in aux_files:
                aux_file = f"{tex_file_path.rsplit('.', 1)[0]}{ext}"
                aux_file_path = os.path.join(output_dir, aux_file)
                if os.path.exists(aux_file_path):
                    os.remove(aux_file_path)

        pdf_path = os.path.join(output_dir, f"{base_name}.pdf")
        print(f"PDF generated successfully: {pdf_path}")
        return pdf_path
    except subprocess.CalledProcessError as e:
        print(f"Error rendering PDF: {e}")
        return None
    
def escape_latex(text):
    """
    Escapes special LaTeX characters in a given string.

    Args:
    text (str): The input string to escape.

    Returns:
    str: The escaped string suitable for LaTeX.
    """
    special_chars = {
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
        '^': r'\^{}',
        '\\': r'\textbackslash{}',
    }
    return ''.join(special_chars.get(c, c) for c in text)

