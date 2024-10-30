# Minify and compress HTML, CSS, and JS files into a single html file and gzip it
import os
import sys
import gzip
import base64
import shutil
import argparse
import minify_html
import htmlmin
import bs4
import markdown2

temp_dir = 'temp'
output_dir = 'output'

# delete the temp and output directories if they exist
if os.path.exists(temp_dir):
    shutil.rmtree(temp_dir)
if os.path.exists(output_dir):
    shutil.rmtree(output_dir)

# make the temp and output directories
os.mkdir(temp_dir)
os.mkdir(output_dir)

# ask the user for a html file
def ask_for_html_file():
    # return "E:\\dev\\tinyMarkdown\\page.html"
    html_file = input('Enter the path to the html file: ')
    if not os.path.exists(html_file):
        print('File does not exist')
        return ask_for_html_file()
    return html_file

# get all linked css and js files (relative paths and URLs), and their contents. Note the order of the files for later
def get_linked_files(html_file):
    linked_files = {
        'css': {},
        'js': {}
    }
    with open(html_file, 'r', encoding='utf-8') as f:
        html = f.read()

    soup = bs4.BeautifulSoup(html, 'html.parser')

    # Find all CSS files
    css_files = soup.find_all('link', rel='stylesheet')
    for index, link in enumerate(css_files):
        href = link.get('href')
        # check if its a valid file or URL
        if str(href).startswith('http') or str(href).endswith('.css'):
            print(href)
            linked_files['css'][f'css_{index}'] = href
            link.replace_with(f'{{{{css_{index}}}}}')

    # Find all JS files
    js_files = soup.find_all('script', src=True)
    for index, script in enumerate(js_files):
        src = script.get('src')
        if str(src).startswith('http') or str(src).endswith('.js'):
            print(src)
            linked_files['js'][f'js_{index}'] = src
            script.replace_with(f'{{{{js_{index}}}}}')

    # Save the modified HTML
    with open(f'{temp_dir}/{file_name}.html', 'w', encoding='utf-8') as f:
        f.write(str(soup))

    return linked_files, str(soup)

def getFile(url):
    import requests
    r = requests.get(url)
    return r.text

# get the contents of all linked files and embed them in the HTML
def embed_linked_files(linked_files, html, html_file):
    # cd into the directory of the HTML file
    current_dir = os.getcwd()
    os.chdir(os.path.dirname(html_file))

    for key, value in linked_files['css'].items():
        if value.startswith('http'):
            linked_files['css'][key] = getFile(value)
            continue
        with open(value, 'r', encoding='utf-8') as f:
            linked_files['css'][key] = f.read()

    for key, value in linked_files['js'].items():
        if value.startswith('http'):
            linked_files['js'][key] = getFile(value)
            continue
        with open(value, 'r', encoding='utf-8') as f:
            linked_files['js'][key] = f.read()

    for key, value in linked_files['css'].items():
        html = html.replace(f'{{{{css_{key.split("_")[1]}}}}}', f'<style>{value}</style>')

    for key, value in linked_files['js'].items():
        html = html.replace(f'{{{{js_{key.split("_")[1]}}}}}', f'<script>{value}</script>')

    # cd back to the original directory
    os.chdir(current_dir)
    # save the modified HTML as a new file
    with open(f'{temp_dir}/{file_name}_embedded.html', 'w', encoding='utf-8') as f:
        f.write(html)

    return html

def buildMarkdown(html):
    # find all <page> tags and convert them to HTML
    soup = bs4.BeautifulSoup(html, 'html.parser')
    markdowns = soup.find_all('page')
    for markdown in markdowns:
        # get the text inside the <page> tag
        markdown_text = markdown.get_text()
        print("Original Markdown Text:")
        print(markdown_text)
        
        # remove the indentation (spaces or tab) before the # to make it work, but do not remove line breaks
        cleanMD = str(markdown_text).replace('\n ', '\n').replace('\n\t', '\n')
        print("Cleaned Markdown Text:")
        print(cleanMD)
        
        # convert the cleaned markdown to HTML
        converted_html = markdown2.markdown(str(cleanMD), extras=[
            'fenced-code-blocks', 'tables', 'strike', 'footnotes', 'metadata', 'lists', 'task_list', 'code-friendly', 'cuddled-lists', 'pyshell', 'code-color'
        ])
        
        # replace the content of the <page> tag with the converted HTML
        markdown.clear()
        markdown.append(bs4.BeautifulSoup(converted_html, 'html.parser'))

    html = str(soup)
    
    # save the modified HTML
    with open(f'{temp_dir}/{file_name}_markdown.html', 'w', encoding='utf-8') as f:
        f.write(html)

    return html

def minify(html):
    # minify the HTML
    # using bs4 get all <page> tags and save them to a list (they will NOT be minified)
    soup = bs4.BeautifulSoup(html, 'html.parser')
    pages = soup.find_all('page')
    pageDivs = {}
    for index, page in enumerate(pages):
        pageDivs[f'page_{index}'] = page
        page.replace_with(f'{{{{page_{index}}}}}')
    html = str(soup)


    minified_html = minify_html.minify(html, minify_js=True, remove_processing_instructions=True)

    # get the <page> tags back
    for key, value in pageDivs.items():
        minified_html = minified_html.replace(f'{{{{page_{key.split("_")[1]}}}}}', str(value))


    # save the minified HTML
    with open(f'{temp_dir}/{file_name}_minified.html', 'w', encoding='utf-8') as f:
        f.write(minified_html)
    
    # compress the minified HTML
    with open(f'{temp_dir}/{file_name}_minified.html', 'rb') as f_in:
        with gzip.open(f'{output_dir}/{file_name}.html.gz', 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    
    return minified_html

def build_html(html):
    # compress the HTML with zlib
    html = gzip.compress(html.encode('utf-8'))
    compressed_html = base64.b64encode(html).decode('utf-8')


    

    template = '''<noscript>Please enable JavaScript</noscript><script>const base64GzipString="''' + compressed_html + '''";async function decompressGzipString(e){const t=atob(e),n=new Uint8Array(t.length);for(let e=0;e<t.length;e++)n[e]=t.charCodeAt(e);const r=new ReadableStream({start(e){e.enqueue(n),e.close()}}),o=new DecompressionStream("gzip"),c=[],a=r.pipeThrough(o).getReader();try{for(;;){const{done:e,value:t}=await a.read();if(e)break;c.push(t)}const e=new Uint8Array(c.reduce(((e,t)=>e.concat(Array.from(t))),[]));insertHtml((new TextDecoder).decode(e))}catch(e){insertHtml("Decompressing Error: "+e)}}function insertHtml(e){document.open(),document.write(e),document.close()}decompressGzipString(base64GzipString);</script>'''

    # save the final HTML
    with open(f'{output_dir}/{file_name}.html', 'w', encoding='utf-8') as f:
        f.write(template)


def main():
    html_file = ask_for_html_file()
    global file_name 
    file_name = os.path.basename(html_file).replace('.html', '')
    linked_files, html = get_linked_files(html_file)
    print(linked_files)
    html = embed_linked_files(linked_files, html, html_file)

    html = buildMarkdown(html)

    html = minify(html)

    build_html(html)
    
    # calculate the size of the original and compressed files
    original_size = os.path.getsize(f'{temp_dir}/{file_name}_embedded.html')
    compressed_size = os.path.getsize(f'{output_dir}/{file_name}.html.gz')

    

    print('Done')
    print(f'File is now {100 - (compressed_size/original_size*100):.2f}% smaller than the original! ({original_size} bytes -> {compressed_size} bytes)')
    print(f'Output file: {output_dir}/index.html')



if __name__ == '__main__':
    main()