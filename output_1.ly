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
 \new Voice { \new Voice { \key g \major 
                c' 8  
                cis' 8  
                ees' 8  
                a' 8  
                bes' 8  
                a' 8  
                bes' 8  
                gis' 8  
                e' 4  
                a' 4  
                bes' 4  
                a' 4  
                gis' 8  
                bes' 8  
                ees' 8  
                g' 8  
                g' 8  
                g' 8  
                a' 8  
                ees' 8  
                d' 4  
                a' 4  
                bes' 4  
                f' 4  
                 } 
               
 
           } 
         
 
  } 
 
\paper { }
\layout {
  \context {
    \override VerticalAxisGroup.remove-first = ##t
  }
 }
 
