import streamlit as st

import streamlit as st

class DisplayMarkdown:
    def __init__(self, color="#737578", font_size="16px", tag="h2", text_align="left", italic=False):
        self.color = color
        self.font_size = font_size
        self.tag = tag
        self.text_align = text_align
        self.italic = italic  # new default option

    def display(self, text, color=None, font_size=None, tag=None, text_align=None, italic=None):
        # Use the provided values or fall back to defaults
        color = color if color is not None else self.color
        font_size = font_size if font_size is not None else self.font_size
        tag = tag if tag is not None else self.tag
        text_align = text_align if text_align is not None else self.text_align
        italic = italic if italic is not None else self.italic

        style = f"color:{color}; font-size:{font_size}; text-align:{text_align};"
        if italic:
            style += " font-style: italic;"

        markdown_html = f"<{tag} style='{style}'>{text}</{tag}>"
        st.markdown(markdown_html, unsafe_allow_html=True)


display_md = DisplayMarkdown()