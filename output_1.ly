\version "2.24" 
\include "lilypond-book-preamble.ly"
    
color = #(define-music-function (parser location color) (string?) #{
        \once \override NoteHead #'color = #(x11-color color)
        \once \override Stem #'color = #(x11-color color)
        \once \override Rest #'color = #(x11-color color)
        \once \override Beam #'color = #(x11-color color)
     #})
    
\header { } 
\score  { 
 \new Voice { \new Voice { \key cis \major 
                f' 8  
                ees' 8  
                cis' 4  
                gis' 4  
                bes' 4  
                cis' 4  
                f' 4  
                ees' 8  
                c' 8  
                cis' 8  
                f' 8  
                ees' 8  
                c' 8  
                cis' 8  
                ees' 8  
                cis' 8  
                f' 8  
                ees' 4  
                ees' 4  
                f' 8  
                ees' 8  
                cis' 4  
                gis' 4  
                 } 
               
 
           } 
         
 
  } 
 
\paper { }
\layout {
  \context {
    \override VerticalAxisGroup.remove-first = ##t
  }
 }
 
