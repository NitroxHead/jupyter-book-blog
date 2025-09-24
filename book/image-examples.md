# Working with Images in Blog Posts

*March 17, 2024*

This post demonstrates various ways to include and format images in your Jupyter Book blog posts, from basic markdown syntax to advanced MyST features.

## Basic Image Inclusion

### Standard Markdown Syntax

The simplest way to include an image:

![Sample landscape](../images/posts/image-examples/sample-landscape.jpg)

*A beautiful landscape photograph demonstrating basic image embedding.*

### Portrait Orientation

Images automatically adapt to different aspect ratios:

![Sample portrait](../images/posts/image-examples/sample-portrait.jpg)

*Portrait-oriented images work seamlessly with the responsive design.*

## Advanced Image Features with MyST

### Controlled Sizing

You can control image dimensions using MyST figure directives:

:::{figure} ../images/posts/image-examples/sample-square.jpg
:width: 300px
:align: center

A square image with controlled width (300px)
:::

### Aligned Images

#### Left Alignment

:::{figure} ../images/posts/image-examples/sample-portrait.jpg
:width: 200px
:align: left

This image is aligned to the left with text wrapping around it. This is useful for creating magazine-style layouts where you want text to flow around smaller images. The content continues to flow naturally around the positioned image.
:::

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.

#### Right Alignment

:::{figure} ../images/posts/image-examples/sample-square.jpg
:width: 200px
:align: right

This image is aligned to the right, creating an attractive layout with flowing text on the left side.
:::

Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

#### Center Alignment

:::{figure} ../images/posts/image-examples/sample-landscape.jpg
:width: 500px
:align: center
:name: centered-landscape

A centered landscape image with custom sizing
:::

### Numbered Figures with References

You can create numbered figures and reference them in your text:

:::{figure} ../images/posts/image-examples/sample-portrait.jpg
:width: 350px
:align: center
:name: fig-portrait-example

Sample portrait photograph with figure numbering
:::

As shown in {numref}`fig-portrait-example`, numbered figures can be referenced throughout your text using MyST cross-references.

## Image Galleries

### Side-by-Side Images

You can create image galleries using grid layouts:

::::{grid} 2
:::{grid-item}
:::{figure} ../images/posts/image-examples/sample-landscape.jpg
:width: 100%

Landscape orientation
:::
:::

:::{grid-item}
:::{figure} ../images/posts/image-examples/sample-portrait.jpg
:width: 100%

Portrait orientation
:::
:::
::::

### Three-Column Gallery

::::{grid} 3
:::{grid-item}
:::{figure} ../images/posts/image-examples/sample-landscape.jpg
:width: 100%

Image 1
:::
:::

:::{grid-item}
:::{figure} ../images/posts/image-examples/sample-square.jpg
:width: 100%

Image 2
:::
:::

:::{grid-item}
:::{figure} ../images/posts/image-examples/sample-portrait.jpg
:width: 100%

Image 3
:::
:::
::::

## Image Organization Best Practices

### Directory Structure

For this blog template, images are organized as follows:

```
images/
├── general/           # Site-wide images (logo, banner, etc.)
│   ├── logo.png
│   └── banner.jpg
└── posts/            # Post-specific images
    ├── post-name-1/  # Each post gets its own folder
    │   ├── figure-1.jpg
    │   ├── figure-2.png
    │   └── diagram.svg
    └── post-name-2/
        └── chart.png
```

### File Naming Conventions

- Use descriptive names: `linear-regression-results.png` instead of `image1.png`
- Use hyphens for spaces: `data-preprocessing-pipeline.jpg`
- Include figure numbers for academic papers: `figure-01-methodology.svg`

### Supported Formats

Jupyter Book supports various image formats:

- **JPEG/JPG**: Best for photographs
- **PNG**: Best for graphics with transparency
- **SVG**: Best for scalable diagrams and illustrations
- **GIF**: Supported for animations (use sparingly)
- **WebP**: Modern format with excellent compression

## Responsive Design

All images in this template are automatically responsive. They scale appropriately on different screen sizes while maintaining their aspect ratios.

### Mobile-First Considerations

:::{figure} ../images/posts/image-examples/sample-landscape.jpg
:width: 100%
:align: center

This image uses 100% width and will scale perfectly on mobile devices
:::

## Advanced Styling

### Custom Classes

You can add custom CSS classes to images for specialized styling:

:::{figure} ../images/posts/image-examples/sample-square.jpg
:width: 300px
:align: center
:class: bordered-image

Custom styled image with border (requires CSS definition)
:::

### Captions with Markdown

:::{figure} ../images/posts/image-examples/sample-portrait.jpg
:width: 400px
:align: center

**Bold caption** with *italic text* and [links](https://example.com) are fully supported in figure captions. You can even include `code` snippets!
:::

## Image SEO Best Practices

1. **Alt Text**: Always include descriptive alt text
2. **Meaningful Filenames**: Use descriptive file names
3. **Appropriate Sizing**: Optimize images for web use
4. **Format Selection**: Choose the right format for the content

### Example with Good Alt Text

![Data visualization showing the correlation between temperature and ice cream sales over a 12-month period, with temperature on the x-axis ranging from 0-40°C and sales on the y-axis ranging from 0-1000 units](../images/posts/image-examples/sample-landscape.jpg)

## Performance Considerations

- **File Size**: Keep images under 500KB when possible
- **Dimensions**: Don't use images larger than needed
- **Lazy Loading**: Jupyter Book includes lazy loading by default
- **Caching**: Images are cached by browsers for better performance

## Conclusion

This blog template provides excellent support for images through:

✅ **Flexible Sizing**: Control dimensions precisely
✅ **Responsive Design**: Automatic scaling across devices
✅ **Advanced Layouts**: Grids, galleries, and alignment options
✅ **Cross-References**: Numbered figures with MyST syntax
✅ **Organized Structure**: Post-specific image folders
✅ **SEO Friendly**: Proper alt text and naming conventions

The combination of standard Markdown and MyST extensions gives you complete control over how images appear in your blog posts.

---

*This example demonstrates comprehensive image handling capabilities in Jupyter Book with MyST Markdown.*