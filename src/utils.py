import re
from textnode import *
from leafnode import *
from blocktype import *

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b",text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code",text_node.text)
        case TextType.IMAGE:
            return LeafNode("img", None, props={"src":text_node.url, "alt":text_node.text})
        case TextType.LINK:
            return LeafNode("a",text_node.text,props={"href":text_node.url} )
        case _:
            raise ValueError(f"invalid text type: {text_node.text_type}")


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    # print(old_nodes)
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

def split_nodes_image(old_nodes):
    # print("Extracting images")
    # print("olds nodes: {old_nodes}")
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        images = extract_markdown_images(old_node.text)
        # print(f"Images found:{images} for text:{old_node.text}")

        if len(images) == 0:
            new_nodes.append(old_node)
            continue

        old_text = old_node.text
        for image in images:
            delimeter = f"![{image[0]}]({image[1]})"

            text, rest = old_text.split(delimeter,1)
            # print(f"After split text = {text}, rest = {rest}")
            if text != "":
                new_nodes.append(TextNode(text,TextType.TEXT))
            else:
                new_nodes.append(old_node)
       
            new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
            old_text = rest

        if old_text != "":
            new_nodes.append(TextNode(old_text,TextType.TEXT))

    return new_nodes
    
def split_nodes_link(old_nodes):
    # print("Exxtracting Links")
    # print(f"Old Nodes: {old_nodes}")
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        links = extract_markdown_links(old_node.text)

        # print(f"Links in: {old_node.text} links: {links}")
        if len(links) == 0:
            new_nodes.append(old_node)
            continue

        old_text = old_node.text
        for link in links:
            delimeter = f"[{link[0]}]({link[1]})"

            text, rest = old_text.split(delimeter,1)
            if text != "":
                new_nodes.append(TextNode(text,TextType.TEXT))
            old_text = rest

            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))

        if old_text != "":
            new_nodes.append(TextNode(old_text,TextType.TEXT))

    return new_nodes


def extract_markdown_images(text):
    images = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return images

def extract_markdown_links(text):
    links = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return links

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    # print(nodes)
    nodes = split_nodes_delimiter(nodes,"**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes,"_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes,"`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    # print(nodes)
    return nodes

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    blocks = list(map(lambda x: x.strip(),filter(lambda x: x != "", blocks)))
    return blocks


def block_to_block_type(markdown_block):
    if re.match(r"^#{1,6} ",markdown_block):
        return BlockType.HEADING
    
    if  markdown_block[0:3] == "```" and markdown_block[len(markdown_block) - 3:] == "```":
        return BlockType.CODE
    
    lines = markdown_block.split("\n")
    isQuote = True
    for line in lines:
        if line[0:1] != ">":
            isQuote = False
            break
    if isQuote:
        return BlockType.QUOTE

    isUnorderedList = True
    for line in lines:
        if line[0:2] != "- ":
            isUnorderedList = False
            break
    if isUnorderedList:
        return BlockType.UNORDERED_LIST
    
    isOrderedList = True
    listNum = 0
    m = re.compile(r"^\d+[.] ")
    d = re.compile(r"^\d+")

    for line in lines:
        listNum += 1
        if m.match(line):
            n = d.match(line)
            if n != None:
                seq = int(n.group())
                if seq != listNum:
                    isOrderedList = False
                    break
            else:
                isOrderedList = False
                break
        else:
            isOrderedList = False
            break

    if isOrderedList:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH

        
def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)

    for block in blocks:
        block_type = block_to_block_type(block)

        


