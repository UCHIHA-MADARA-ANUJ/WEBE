import React from 'react';
// Minimal stub for next/link in jsdom smoke tests
export default function Link({ children, href, ...rest }) {
  return React.createElement('a', { href, ...rest }, children);
}
