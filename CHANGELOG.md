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
