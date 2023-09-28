---
categories: ["streamlit"]
tags: ["streamlit"] 
title: "Create a basic webpage"
linkTitle: "Create a basic webpage"
description: >
  Create a basic Streamlit webpage
---
> This was performed on Windows 11

### Install Streamlit
- Install Streamlit

```terminal
pip install streamlit
```

### Create a Python file
- Put it in a working directory
- Name the file `app.py`

### Create some simple initial content and test
- In the `app.py` file create the following Python code.

```python
import streamlit as st

# ---- CONSTANTS ----
STREAMLIT_URL = "https://www.streamlit.io"

# ---- PAGE CONFIG ----
st.set_page_config(page_title="Basic Webpage", layout="wide")

# ---- HEADER SECTION ----
with st.container():
    st.subheader("This is a basic Streamlit webpage")
    st.title("This is to demonstrate Streamlit")
    st.write("Streamlit is an open-source Python library designed to help developers "
             "create interactive and aesthetically pleasing web applications for data science "
             "and machine learning projects with minimal effort.")
    st.markdown(f"[Learn More >]({STREAMLIT_URL})", unsafe_allow_html=True)
```

To test the code in a Terminal browse to the working directory and run:

```terminal
streamlit run .\app.py
```

### Add 2 columns with some text and an animation
- Add the following section to create two columns. 
- The first column on the left of the screen will have text
- The second column on the right of the screen will have an animation; detailed in the next section.

```python
# ---- COLUMN SECTION ----
with st.container():
    st.write("---")
    left_column, right_column = st.columns(2)
    
    with left_column:
        st.header("Left column header")
        st.write("""
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
            Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
            Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. 
            Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
            """)
```

#### Add an animation to the second column
- Install the streamlit Lottie library on your workstation

```terminal
pip install streamlit-lottie
```

- Install the requests library

```terminal
pip install requests
```

- Then add the import to the `app.py` file

```python
import requests
import streamlit as st
from streamlit_lottie import st_lottie
```

- Create a function to get the JSON data from the Lottie URI

```python
# ---- FUNCTION TO LOAD LOTTIE JSON DATA ----
def load_lottieurl(url):
    """Loads lottie JSON data from a given URL."""
    try:
        r = requests.get(url)
        r.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
        return r.json()
    except requests.RequestException as e:
        st.error(f"Failed to load Lottie URL: {str(e)}")
        return None
```

- Go to the lottie file website and choose an animation
- Once loaded, copy the animation asset link URI
- In the  `app.py` file create a new constants section and add the asset link URI

```python
# ---- CONSTANTS ----
LOTTIE_URL = "https://lottie.host/2011bba0-0444-4c05-92e2-9e1ec63fef08/2CGPse9h3m.json"
```

- Add the function in front of the lottie_coding URI

```python
# ---- LOAD THE LOTTIE ASSET ----
lottie_coding = load_lottieurl(LOTTIE_URL)
```

### Use CSS style
- Create a new folder and file `./style/style.css`
- Insert the following code which will style the website

```css
/* Hide Streamlit Branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
```

- In the `app.py` file create a new function block
- This function will get the style.css file and convert it to markdown

```python
# ---- FUNCTION TO INSERT A LOCAL CSS FILE ----
def local_css(file_name):
    """Loads local CSS file into the app."""
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
```

- Define the path to the CSS file in the constants section

```python
CSS_FILE = "style/style.css"
```

- Call the function and define the path to the CSS file

```python
# ---- LOAD THE LOCAL CSS FILE ----
local_css(CSS_FILE)
```

### Use a Streamlit theme to change the webpage colors
- Create a new folder and file `./.streamlit/config.toml`
- Insert the following code which will style the website

```css
[theme]

# Primary accent for interactive elements
primaryColor = '#E694FF'

# Background color for the main content area
backgroundColor = '#00172B'

# Background color for sidebar and most interactive widgets
secondaryBackgroundColor = '#0083B8'

# Color used for almost all text
textColor = '#FFFFFF'

# Font family for all text in the app, except code blocks
# Accepted values (serif | sans serif | monospace) 
# Default: "sans serif"
font = "sans serif"
```

### Final code
Put together the final code looks like this:

```
+---working-directory
|   +---.streamlit
|   |       config.toml
|   +---style
|   |       style.css
|   app.py
```

{{< tabpane persistLang=false >}}
{{< tab header="Streamlit webpage" disabled=true />}}
{{< tab header="app.py" lang="python" >}}
import requests
import streamlit as st
from streamlit_lottie import st_lottie

# ---- CONSTANTS ----
LOTTIE_URL = "https://lottie.host/2011bba0-0444-4c05-92e2-9e1ec63fef08/2CGPse9h3m.json"
STREAMLIT_URL = "https://www.streamlit.io"
CSS_FILE = "style/style.css"

# ---- PAGE CONFIG ----
st.set_page_config(page_title="Basic Webpage", layout="wide")

# ---- FUNCTION TO LOAD LOTTIE JSON DATA ----
def load_lottieurl(url):
    """Loads lottie JSON data from a given URL."""
    try:
        r = requests.get(url)
        r.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
        return r.json()
    except requests.RequestException as e:
        st.error(f"Failed to load Lottie URL: {str(e)}")
        return None

# ---- FUNCTION TO INSERT A LOCAL CSS FILE ----
def local_css(file_name):
    """Loads local CSS file into the app."""
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ---- LOAD THE LOCAL CSS FILE ----
local_css(CSS_FILE)

# ---- LOAD THE LOTTIE ASSET ----
lottie_coding = load_lottieurl(LOTTIE_URL)

# ---- HEADER SECTION ----
with st.container():
    st.subheader("This is a basic Streamlit webpage")
    st.title("This is to demonstrate Streamlit")
    st.write("Streamlit is an open-source Python library designed to help developers "
             "create interactive and aesthetically pleasing web applications for data science "
             "and machine learning projects with minimal effort.")
    st.markdown(f"[Learn More >]({STREAMLIT_URL})", unsafe_allow_html=True)

# ---- COLUMN SECTION ----
with st.container():
    st.write("---")
    left_column, right_column = st.columns(2)
    
    with left_column:
        st.header("Left column header")
        st.write("""
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
            Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
            Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. 
            Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
            """)
    
    with right_column:
        if lottie_coding:
            st_lottie(lottie_coding, height=300, key="coding")


{{< /tab >}}
{{< tab header="style.css" lang="css" >}}
/* Hide Streamlit Branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
{{< /tab >}}

{{< tab header="config.toml" lang="toml" >}}
[theme]

# Primary accent for interactive elements
primaryColor = '#E694FF'

# Background color for the main content area
backgroundColor = '#00172B'

# Background color for sidebar and most interactive widgets
secondaryBackgroundColor = '#0083B8'

# Color used for almost all text
textColor = '#FFFFFF'

# Font family for all text in the app, except code blocks
# Accepted values (serif | sans serif | monospace) 
# Default: "sans serif"
font = "sans serif"
{{< /tab >}}
{{< /tabpane >}}


## References

<a href="https://www.streamlit.io/" target="_blank">Streamlit</a>

<a href="https://blog.streamlit.io/introducing-theming/" target="_blank">Streamlit Theme</a>

<a href="https://github.com/Sven-Bo/personal-website-streamlit" target="_blank">Sven-Bo GitHub repo</a>

<a href="https://lottiefiles.com/" target="_blank">Lottie Files</a>