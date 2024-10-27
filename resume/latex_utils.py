import json
import subprocess
import os

def convert_latex_to_pdf(tex_file_path, output_dir):
    """
    Renders a LaTeX file to PDF using pdflatex in non-interactive mode.
    
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
        
        # Set environment variables to prevent interactive prompts
        env = os.environ.copy()
        env['TEXFOT'] = 'false'
        env['MAX_PRINT_LINE'] = '10000'
        env['ERROR_LINE'] = '254'
        env['HALT_ON_ERROR'] = 'true'
        
        # Common pdflatex arguments for non-interactive mode
        pdflatex_args = [
            'pdflatex',
            '-interaction=nonstopmode',
            '-halt-on-error',
            '-file-line-error',
            '-no-shell-escape',
            '-output-directory', output_dir,
            tex_file_path
        ]
        
        # Run pdflatex twice to ensure all references are resolved
        for _ in range(2):
            subprocess.run(
                pdflatex_args,
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                env=env,
                timeout=30  # Add timeout to prevent hanging
            )
        
        # Delete auxiliary files
        aux_files = ['.aux', '.log', '.out', '.fls', '.fdb_latexmk']
        for ext in aux_files:
            aux_file = f"{base_name}{ext}"
            aux_file_path = os.path.join(output_dir, aux_file)
            if os.path.exists(aux_file_path):
                os.remove(aux_file_path)
        
        pdf_path = os.path.join(output_dir, f"{base_name}.pdf")
        
        # Verify PDF was actually generated
        if not os.path.exists(pdf_path):
            print(f"PDF file was not generated at {pdf_path}")
            return None
            
        print(f"PDF generated successfully: {pdf_path}")
        return pdf_path
        
    except subprocess.TimeoutExpired:
        print("PDF generation timed out after 30 seconds")
        return None
    except subprocess.CalledProcessError as e:
        print(f"Error rendering PDF: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
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

