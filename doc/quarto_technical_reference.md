# QUARTO TECHNICAL SYNTAX REFERENCE (LLM OPTIMIZED)

## 1. BLOCK STRUCTURE & DIVS
Syntax for generic containers (Divs) and inline styles (Spans).

### Divs (Blocks)
Use `:::` to delimit blocks.
```markdown
::: {.class #id attribute="value"}
Content
:::
````

### Spans (Inline)

Use `[]` followed by `{}`.

```markdown
[Text content]{.class key="val"}
```

-----

## 2\. CALLOUT BLOCKS

Strict taxonomy for admonitions.

### Syntax

```markdown
::: {.callout-type}
## Optional Title
Content goes here.
:::
```

### Supported Types

1.  `note` (Blue)
2.  `tip` (Green)
3.  `important` (Red/Bold)
4.  `caution` (Yellow)
5.  `warning` (Red/High Alert)

### Options

  * **Collapsible:** `::: {.callout-note collapse="true"}` (Collapsed by default) or `collapse="false"`.
  * **Appearance:** `appearance="simple"` (minimalist) or `appearance="minimal"` (no icon/color).
  * **No Icon:** `icon=false`.

-----

## 3\. FIGURES & IMAGES

Syntax for embedding and styling images.

### Basic Syntax

`![Caption Text](path/to/image.png){#fig-id attributes}`

### Key Attributes

| Attribute | Example | Description |
| :--- | :--- | :--- |
| **ID (Required for Ref)** | `{#fig-myimage}` | Must start with `fig-`. |
| **Width/Height** | `width=50%`, `height=4in` | Resizing. |
| **Alignment** | `fig-align="left"` | `left`, `center`, `right`. |
| **Alt Text** | `fig-alt="Description"` | Accessibility text. |
| **Lightbox** | `{.lightbox}` | Enables interactive zoom (HTML). |

### Subfigures (Layouts)

Group images using a Div with `layout-ncol`.

```markdown
::: {#fig-main layout-ncol=2}
![Subcaption A](img1.png){#fig-a}
![Subcaption B](img2.png){#fig-b}

Main Caption
:::
```

-----

## 4\. TABLES

Markdown pipe tables and grid tables.

### Syntax

```markdown
| Col1 | Col2 |
|------|------|
| A    | B    |

: Caption Text {#tbl-id}
```

### Attributes

  * **Column Widths:** `: {tbl-colwidths="[60,40]"}` (Percentages).
  * **ID:** Must start with `{#tbl-...}`.

-----

## 5\. CROSS-REFERENCES

Rules for linking internal content.

### ID Prefixes (Strict)

Target elements MUST use these prefixes in their `{ #id }`.

| Type | Prefix | Reference Syntax | Example |
| :--- | :--- | :--- | :--- |
| **Figures** | `fig-` | `@fig-name` | `See @fig-structure` |
| **Tables** | `tbl-` | `@tbl-name` | `Data in @tbl-results` |
| **Sections** | `sec-` | `@sec-name` | `See @sec-intro` |
| **Equations** | `eq-` | `@eq-name` | `Formula @eq-std` |
| **Listings** | `lst-` | `@lst-name` | `Code in @lst-main` |
| **Theorems** | `thm-` | `@thm-name` | `Proof in @thm-1` |

### Syntax Rules

  * **Definition:** `{#fig-name}` (Inside attributes).
  * **Usage:** `@fig-name` (In text).
  * **Grouped:** `[@fig-a; @fig-b]`.
  * **Capitalized:** `@Fig-name` -\> "Figure 1".

-----

## 6\. ARTICLE LAYOUT & COLUMNS

Classes to control content width and positioning (Marginalia/Tufte style).

### Column Classes (Divs & Chunks)

Apply to Divs `::: {.class}` or Code Chunks `#| column: class`.

| Class / Option | Effect |
| :--- | :--- |
| `.column-body` | Standard width (default). |
| `.column-body-outset` | Slightly wider than body text. |
| `.column-page` | Wider, spans main column + margin. |
| `.column-screen` | Full screen width (bleed). |
| `.column-margin` | Places content in the right margin. |

### Margin Elements

  * **Text/Images:**
    ```markdown
    ::: {.column-margin}
    This is a side note or image.
    :::
    ```
  * **Figures (Code):** `#| column: margin` or `#| fig-column: margin`.
  * **Captions only:** `#| cap-location: margin` (Figure in body, caption in margin).
  * **Footnotes/Citations:** Set in YAML `reference-location: margin`.

-----

## 7\. CODE BLOCKS & EXECUTION OPTIONS

Configuration for executable chunks (Python/R).

### Syntax

Use YAML style options inside the block, prefixed with `#|`.

````python
```{python}
#| label: fig-plot
#| fig-cap: "My Plot"
#| echo: false

import matplotlib.pyplot as plt
````

````

### Common Options
| Option | Values | Description |
| :--- | :--- | :--- |
| `label` | `fig-xyz`, `tbl-xyz` | Unique ID for cross-ref. |
| `echo` | `true`, `false`, `fenced` | Show source code in output. |
| `eval` | `true`, `false` | Execute the code. |
| `output` | `true`, `false`, `asis` | Show output (stdout/plot). |
| `warning` | `true`, `false` | Show warnings. |
| `error` | `true`, `false` | Show errors. |
| `layout-ncol` | Integer (e.g., 2) | Arrange multiple plots in columns. |

---

## 8. MATH & EQUATIONS
LaTeX syntax support.

* **Inline:** `$E = mc^2$`
* **Display:** `$$E = mc^2$$`
* **Referenceable:**
    ```markdown
    $$
    x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}
    $$ {#eq-quadratic}
    ```

---

## 9. DIAGRAMS (MERMAID)
Native diagram support.

```markdown
```{mermaid}
flowchart LR
  A[Start] --> B{Decision}
  B -- Yes --> C[OK]
  B -- No --> D[Error]
````

```
