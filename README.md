# obsidianki2

Obsidianki is an [Anki](https://github.com/ankitects/anki) plugin that allows you to import your obsidian vault into Anki. It can generate clozes for your cards with bold(`**bold**`), italics(`**italics**`), highlight(`==highlight==`), wiki-links(`[[wikilinks]]`), inline code (`code`), inline math(`\(\dfrac{1}{2}\)`), and display math(`\[\dfrac{1}{2}\]`).

*Note that this add-on is written for Mac and takes advantage of Mac's url scheme feature. I don't know if it will work on windows or linux.*

## Progress

### TODOs

- [x] Add support for link back to Obsidian
- [x] Add support for metadata and tags
- [x] Work on a user manual
- [ ] Work on the user interface


## Special Note

For me, coding this project was very challenging. I have never learned python, and my only knowledge of programming come from the AP Computer Science A exam LOL. For about five days or so, I spend all my time working on it, trying my best to look at the source code of Anki and other plugins.

I know that my code must be really bad, but for now I don't have the ability to improve it. Contributions to this project are very warmly welcomed, and I sincerely hope that some of you guys could teach me about how to write good code. Meanwhile, I will spend some time these days adding comments to my notes to share with you my thinking when writing the code. I hope that though sharing this with everyone, new people like me could benefit from sometimes arbitrary codes. Again, I know that my code is good, and the purpose of this act would be merely sharing a green-hand's perspective.

Also, as I have no idea of how to use `qt` to write code for the interface, I may not be able to add a user interface for this for now. (I have spent several days on this project, and I gotta go studying:-). I will check try to come up with a working user interface in the future.

## Standards

To use this template, your notes in Obsidian will have to conform to the following standards:

1. Your notes should follow the following organization structure inside the vault:
	1. First Level: folders
	2. Second Level: notes
	multi-level organization structure is, as of right now (or maybe forever), not supported. You could, however, use a multi-level organization structure, but files in other level will not be imported to Anki. Just Bear this in mind. 
2. Every note name must be stamped with a time-stamp. For example, instead of writing a note called `Obsidianki`, you should stamp it with a ZTK pre-fixer such as this one: `20210103075618 Obsidianki`. This is especially important this add-on uses time-stamp to create the unique identifiers for the notes (so that your note will not be added to the card deck multiple times) and the wiki-links. It would be very convenient if you could have a keyboard expander that automatically fills in the time stamp. <u>For me, I use `Typinator` to automatically creat a time stamp when I type `%ztk`.</u> 
3. Every note should begin with a metadata section, and should begin, after the metadata, with a heading 1. This is largely due to the limitation of [markdown2](https://github.com/trentm/python-markdown2).

## How to Use

To use this add-on, you will have to manually set up a few things. 

### Drag the folder to your Anki Add-ons folder

Download this file as a zip, and unzip it. Drag this folder to your anki Add-ons folder. If you don't know where is your Anki Add-ons folder, you can open Anki. In the menu bar, select `Tools` → `Add-ons`. 

![](https://tva1.sinaimg.cn/large/0081Kckwgy1gma7g4v6uhj30u00mgdyo.jpg)

In the pop-up menu, you will be able to see a button called `View files`. Click on that button, and you will be able to visit your add-ons folder. 

![](https://tva1.sinaimg.cn/large/0081Kckwgy1gma7gxmnc2j30y20omdjx.jpg)


### Change the `settings.py` file

In the Obsidianki2 folder that you just dragged into your add-ons folder, you will see a file called `settings.py`. Inside it are the following code:

```python
vault_name = "Knowledge Base"

path_to_vault = "/Users/xiuxuan/Library/Mobile Documents/iCloud~org~zrey~metion/Documents/Knowledge Base"

whether_to_convert = {"bold": True, "wiki-links": False, "italics": True, "hightlight": False, "inline code": True, "inline math": True, "display math": False}
```

You should change the `vault_name` to the name of your vault folder. If you don't know, you can open Obsidian's vault switcher, and you will be able to notice it on the left. For me, it's `Knowledge Base`

You should change the `path_to_vault` to the path below the `Knowledge Base`'s name. For me, it's `/Users/xiuxuan/Library/Mobile Documents/iCloud~org~zrey~metion/Documents/Knowledge Base`. 

![](https://tva1.sinaimg.cn/large/0081Kckwgy1gma6rjrbd4j310k0u0q9l.jpg)

Now let's look at this line of code:

```python
whether_to_convert = {"bold": True, "wiki-links": False, "italics": True, "hightlight": False, "inline code": True, "inline math": True, "display math": False}
```

This is your settings for deciding whether if a certain type in Markdown needs to be converted to Clozes in Anki. For example, in default setting, `bold` is set to `True`, which means that the bold syntax (`**bold**`) in markdown will be converted to Clozes in Anki. The `wiki-links` is set to false, which means that the wiki-link syntax (`[[20210103075618 Obsidianki]]`) will be not be converted to cloze. *It is recommended that you leave the settings for this as is in this file.*

### Import the `Obsidianki.apkg` file

Double click on the `Obsidianki.apkg` file to import it. This file contains the file template `Obsidianki` that this add-on will use. In the next section, I will explain about the `Obsidianki` template.

### Import from Obsidian

Now, you are all set. All you will need to so for now is to use the add-on. You will need to open Anki, and select `Tools` → `Import from Obsidian` from the menubar.

![](https://tva1.sinaimg.cn/large/0081Kckwgy1gma7jsc6f4j30to0ly4g3.jpg)

> You may notice that in my screenshot, there is a shortcut besides the `Import from Obsidian`. It is **not** a feature of this add-on. However, if you want to add a short-cut to this plug-in, you could click on the Apple logo on your menu bar, and select `system preferences`. In it, click on `Keyboad`, and then go to `Shortcuts` → `App Shortcuts`. There you can add a short cut for this function by typing in `Import from Obsidian` exactly as it is and select your preferred shortcut key combo.

## How it works

Obsidianki imports your files in Obsidian into Anki. It creates a single note for each file in your Obsidian folder. 

### Obsidianki Template

The Obsidianki template is essentially a `Cloze` template, but it has two more fields: `Text` and `ZTK ID` (In Obsidianki, the `Cloze` template's `Text` is renamed to `Cloze`). 

#### `ZTK ID`

The `ZTK ID` field stores your file's ZTK time stamp. You should not change it. This add-on reads the ZTK time stamp in your file name, queries the anki database for notes whose first`ZTK ID` field is equal to the time stamp. If there is a note whose `ZTK ID` matches the `ZTK ID` of your note, the note is overwitten. Otherwise, a new note is added. 

#### `Cloze` and `Text`

Obsidianki detects if your file has generated clozes. If yes, it will be placed into the `Cloze` field. Otherwise, it will not be placed into the `Text` field, and a place holder `{{c1::}}` will be added to the `Cloze` field so that the card would not be considered empty. **If `Text` field has text in it, the `Cloze` field would not show.** Therefore, do not add text to the `Text` field when it doesn't have.

#### `Back Extra`

Stores information in your file's metadata. 

### Cloze Generation

For that file, it reads everything that it has, and see if anything needs to be converted to Cloze cards. It supports converting the following syntaxes into Cloze cards in Anki:

- Bold
- Italics
- Highlight
- Wikilinks
- Inline Code
- Inline Math
- Display Math

By default, bold, italics, inline code, and inline math are converted, while highlight, wikilinks, and display math are not. 

### Wikilink Generation

Obsidianki generates a link back to your Obsidian file by searching through your files in your Obsidian vault. Not that it only supports generating links to exisiting files, not to none-existing ones. However, you can always refresh your database after you added that file. 

As url scheme is a Mac Oly feature, linking back to Obsidian will not work in other systems. 

## Thanks

In Obsidianki, I have used:

- [markdown2](https://github.com/trentm/python-markdown2) for markdown to html conversion
- [pygmentcss](https://github.com/richleland/pygments-css) for code highlighting
- [markdowncss/modest](https://github.com/markdowncss/modest) for markdown style in anki card

Many thanks to [Ankitects](https://github.com/ankitects) for their awesome free [app](https://github.com/ankitects/anki) and great [addon writing manual](https://github.com/ankitects/addon-docs). I also want to thank [W3C School](https://www.w3schools.com/python/default.asp) and [Runoob](https://www.runoob.com) for their python tutorials. 





