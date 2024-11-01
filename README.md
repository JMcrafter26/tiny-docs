
# Tiny Docs

![Banner](https://raw.githubusercontent.com/JMcrafter26/tiny-docs/main/.github/banner.png)

[![GitHub license](https://img.shields.io/github/license/JMcrafter26/tiny-docs)](LICENSE)
[![GitHub issues](https://img.shields.io/github/issues/JMcrafter26/tiny-docs)](https.//github/license/JMcrafter26/tiny-docs)

## What is Tiny Docs
Tiny Docs is a simple and lightweight (single file!) documentation template that allows you to write documentation in markdown and have it rendered as a static site

## Features

- 📄 **Single file** - Just one HTML file!
- 📝 **Markdown** - Write documentation in [markdown](?page=snarkdown)
- 📦 **Zero dependencies** - No need for a build step or package manager. (Although there are tools to make it even smaller)
- 🎨 **Customizable** - Change the CSS to fit your style
- 📱 **Responsive** - Works on all devices
- 🚀 **Fast** - Loads _extremely_ fast

## Use cases

- Personal documentation
- Project documentation
- Software documentation
- _Anything_ that needs documentation
I made this because I wanted a simple way to write documentation and have it in a single file. I hope you find it useful!

## Demo

[Check out the demo](https://raw.githack.com/JMcrafter26/tiny-docs/main/tinydocs.html)

Also check out the [Web Builder](https://raw.githack.com/JMcrafter26/tiny-docs/main/builder/builder.html) (Currently in Beta)

## How to use

> This project is still in development. Some features may not work as expected
1. Download the HTML file (or clone the repo)
1. Open the file in your text editor
1. [Write and customize](https://raw.githack.com/JMcrafter26/tiny-docs/main/builder/builder.html) your documentation

## Planned features

- [ ] 🔎 Search [Halfway done](https://raw.githack.com/JMcrafter26/tiny-docs/main/test/search.html)
- [x] 📖 Table of contents
- [x] 🌐 Full [Offline Suport](#offline-support)
- [ ] 🛠️ Import from GitHub Wiki
- [x] 📝 [Web Builder](https://raw.githack.com/JMcrafter26/tiny-docs/main/builder/builder.html) (Currently in Beta)
- [ ] 📤 Export to PDF/Markdown/HTML

## Advanced usage

### Offline support

> [!NOTE]
> This is only needed if the file is hosted on a server. If you are using it as a local html file, you don't need to do this (it will work offline by default)

Tiny Docs can be used offline. But not only that, it can be used _fully_ offline. This means that you can use it without an internet connection.

To use Tiny Docs offline, you will need to put `sw.js` in the same directory as `tinydocs.html`. This will allow the service worker to cache the page and allow you to use it offline.

> I know that this defeats the purpose of a single file, but it is the only way to make it work offline. And it is still a single file if you don't use it on a server.
        
