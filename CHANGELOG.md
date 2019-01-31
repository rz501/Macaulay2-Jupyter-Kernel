## [0.6.6]
- Clean up asset installation - codemirror and kernel spec.
- Add custom shortcuts.
- Add custom help link.

## [0.6.5]
- Guard against echo in pexpect.
- Added `9,0` as a kernel-restart-and-clear keyboard shortcut.
- Added `debug` interpreter option.
- Added `original` display mode, returning the same output as M2's interactive session,
  making it easy to copy output in text-only context.
- Other small tweaks.

## [0.6.0] Major changes addressing stability and performance
- Rewrote the REPL part:
    * It no longer uses regexes (except for inferring the input \#).
      This had a tremendous effect on stability and speed.
    * Added finer timeout control.
      Now if a statement timeouts, then whole cell execution is interrupted,
      and this is clearly reported to the client.
    * Macaulay2 exceptions and stdout are always printed to the cell's stdout.
      I removed stderr formatting, since it did not fit nicely with the rest.
    * Decoupled the REPL from the kernel-proper class.
      It can now be used directly in Python3. Will add demo later.

## [0.5.2]
- Put codemirror mode in the correct place.
  This fixes GET 404 error that prevented syntax highlighting when running remotely.
  This isn't documented at all but the fix works fine.
- Add comment in Macaulay2 using Cmd-/ or Ctrl-/.

## [0.5.1]
- Add the nbextension to the distribution.

## [0.5.0]
- Capture TIMEOUT exceptions.
- Send ^C control to proc when needed.
- Redirect M2 errors to stderr always.
- Added raw mode.

## [0.4.0]
- Client-side syntax highlighting.

## [0.3.2]
- Added `pretty` display mode.

## [0.3.0] 
- Add robust cell magic support.
- Minor syntax highlighting changes.

## [0.2.3]
- Bug fixes.
- Changed mode `normal` to `default`.
- Syntax hightlight changes.

## [0.2.0] - 2019-01-18
- Stable IO processing. Not aware of bugs or caveats.
- In normal mode, code in cells evaluates the same way as in M2 interactive mode.
- Output now is only presented for the last statement in a block.
  This is intentional and parallels IPython.
  M2 errors still need to be propagated though. See TODO.
- Implements basic cell magic (as IPython does) and configuration.
- Can provide configuration script using `$M2JK_CONFIG`.
- Two output modes: *normal* and *texmacs*. Another one, *pretty*, is commented out. See TODO.
- Modes can be specified in config file at start up, or during execution.
- *normal* is exactly the same as M2 interactive mode.
- *texmacs* prints and renders the output value the way your browser does.
- Timeouts can be set for the allowed delay for a block calculation (plus transport).
  They can be set in a configure script or interactively.
- Profiling didn't show any speed up using byte-strings over regular strings for 
  both matching and transport, so kept current set up.

## [Unreleased]
- Basic implementation. Many bugs.
- Code organized properly as a pip3 module.
- Some highlighting on the client side.
