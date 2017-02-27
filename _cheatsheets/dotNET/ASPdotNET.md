---
title: Using Yeoman to generate a ASP.NET Core app from a template
category: dotNET
tags: .NET C# ASP.NET
---

## Steps

### Install Node.js and npm

To get started with Yeoman, install [Node.js](https://nodejs.org/en/). The installer includes Node.js and [npm](https://www.npmjs.com/).

- for Mac OS X
```bash
brew install node
``` 

- for Windows OS
```bash
choco install nodejs
```


## Install [Yeoman](http://yeoman.io/) and [Bower](https://bower.io/)


```bash
npm install -g yo

npm install -g bower
```

## Install [generator-aspnet](https://www.npmjs.com/package/generator-aspnet)
        
```
npm install -g generator-aspnet
```

Run with 
```
yo aspnet
``

See also: [Building Projects with Yeoman on docs.asp.net](https://docs.microsoft.com/en-us/aspnet/core/client-side/yeoman)


## Optionaly install the [yeoman extension](https://marketplace.visualstudio.com/items?itemName=samverschueren.yo) in Visual Studio Code
