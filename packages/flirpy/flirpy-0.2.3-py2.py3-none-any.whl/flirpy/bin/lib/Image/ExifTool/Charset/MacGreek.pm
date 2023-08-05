#------------------------------------------------------------------------------
# File:         MacGreek.pm
#
# Description:  Mac Greek to Unicode
#
# Revisions:    2010/01/20 - P. Harvey created
#
# References:   1) http://unicode.org/Public/MAPPINGS/VENDORS/APPLE/GREEK.TXT
#
# Notes:        The table omits 1-byte characters with the same values as Unicode
#------------------------------------------------------------------------------
use strict;

%Image::ExifTool::Charset::MacGreek = (
  0x80 => 0xc4, 0x81 => 0xb9, 0x82 => 0xb2, 0x83 => 0xc9, 0x84 => 0xb3,
  0x85 => 0xd6, 0x86 => 0xdc, 0x87 => 0x0385, 0x88 => 0xe0, 0x89 => 0xe2,
  0x8a => 0xe4, 0x8b => 0x0384, 0x8c => 0xa8, 0x8d => 0xe7, 0x8e => 0xe9,
  0x8f => 0xe8, 0x90 => 0xea, 0x91 => 0xeb, 0x92 => 0xa3, 0x93 => 0x2122,
  0x94 => 0xee, 0x95 => 0xef, 0x96 => 0x2022, 0x97 => 0xbd, 0x98 => 0x2030,
  0x99 => 0xf4, 0x9a => 0xf6, 0x9b => 0xa6, 0x9c => 0x20ac, 0x9d => 0xf9,
  0x9e => 0xfb, 0x9f => 0xfc, 0xa0 => 0x2020, 0xa1 => 0x0393, 0xa2 => 0x0394,
  0xa3 => 0x0398, 0xa4 => 0x039b, 0xa5 => 0x039e, 0xa6 => 0x03a0, 0xa7 => 0xdf,
  0xa8 => 0xae, 0xaa => 0x03a3, 0xab => 0x03aa, 0xac => 0xa7, 0xad => 0x2260,
  0xae => 0xb0, 0xaf => 0xb7, 0xb0 => 0x0391, 0xb2 => 0x2264, 0xb3 => 0x2265,
  0xb4 => 0xa5, 0xb5 => 0x0392, 0xb6 => 0x0395, 0xb7 => 0x0396, 0xb8 => 0x0397,
  0xb9 => 0x0399, 0xba => 0x039a, 0xbb => 0x039c, 0xbc => 0x03a6,
  0xbd => 0x03ab, 0xbe => 0x03a8, 0xbf => 0x03a9, 0xc0 => 0x03ac,
  0xc1 => 0x039d, 0xc2 => 0xac, 0xc3 => 0x039f, 0xc4 => 0x03a1, 0xc5 => 0x2248,
  0xc6 => 0x03a4, 0xc7 => 0xab, 0xc8 => 0xbb, 0xc9 => 0x2026, 0xca => 0xa0,
  0xcb => 0x03a5, 0xcc => 0x03a7, 0xcd => 0x0386, 0xce => 0x0388,
  0xcf => 0x0153, 0xd0 => 0x2013, 0xd1 => 0x2015, 0xd2 => 0x201c,
  0xd3 => 0x201d, 0xd4 => 0x2018, 0xd5 => 0x2019, 0xd6 => 0xf7, 0xd7 => 0x0389,
  0xd8 => 0x038a, 0xd9 => 0x038c, 0xda => 0x038e, 0xdb => 0x03ad,
  0xdc => 0x03ae, 0xdd => 0x03af, 0xde => 0x03cc, 0xdf => 0x038f,
  0xe0 => 0x03cd, 0xe1 => 0x03b1, 0xe2 => 0x03b2, 0xe3 => 0x03c8,
  0xe4 => 0x03b4, 0xe5 => 0x03b5, 0xe6 => 0x03c6, 0xe7 => 0x03b3,
  0xe8 => 0x03b7, 0xe9 => 0x03b9, 0xea => 0x03be, 0xeb => 0x03ba,
  0xec => 0x03bb, 0xed => 0x03bc, 0xee => 0x03bd, 0xef => 0x03bf,
  0xf0 => 0x03c0, 0xf1 => 0x03ce, 0xf2 => 0x03c1, 0xf3 => 0x03c3,
  0xf4 => 0x03c4, 0xf5 => 0x03b8, 0xf6 => 0x03c9, 0xf7 => 0x03c2,
  0xf8 => 0x03c7, 0xf9 => 0x03c5, 0xfa => 0x03b6, 0xfb => 0x03ca,
  0xfc => 0x03cb, 0xfd => 0x0390, 0xfe => 0x03b0, 0xff => 0xad,
);

1; # end
