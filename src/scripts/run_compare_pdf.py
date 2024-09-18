import os
import sys

current_dir = os.path.abspath(__file__)
parent_dir = os.path.dirname(current_dir)
grandparent_dir = os.path.dirname(parent_dir)
great_grandparent_dir = os.path.dirname(grandparent_dir)
sys.path.append(parent_dir)
sys.path.append(grandparent_dir)
sys.path.append(great_grandparent_dir)

from tools.tools_utils import generate_comparison_pdf

if __name__ == "__main__":
    generate_comparison_pdf("outputs/pdf/original_long_resume.pdf", "outputs/pdf/output_resume.pdf", "outputs/pdf/compare_diff.pdf")