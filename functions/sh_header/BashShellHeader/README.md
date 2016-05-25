# BashShellHeader
Linux Bash ( GNU Bourne-Again SHell ) Shell Script Header.
```c
/* The color strings used for matched text.
   The user can overwrite them using the deprecated
   environment variable GREP_COLOR or the new GREP_COLORS.  */
static const char *selected_match_color = "01;31";      /* bold red */
static const char *context_match_color  = "01;31";      /* bold red */

/* Other colors.  Defaults look damn good.  */
static const char *filename_color = "35";       /* magenta */
static const char *line_num_color = "32";       /* green */
static const char *byte_num_color = "32";       /* green */
static const char *sep_color      = "36";       /* cyan */
static const char *selected_line_color = "";    /* default color pair */
static const char *context_line_color  = "";    /* default color pair */

```
