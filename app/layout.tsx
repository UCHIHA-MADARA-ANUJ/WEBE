import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'STRATA — The interface should follow the work.',
  description:
    'A behaviour-adaptive workspace that rebuilds its own layout, hierarchy and workflows around how you work. Same project, different structures.',
  openGraph: {
    title: 'STRATA — The interface should follow the work.',
    description:
      'A website with no fixed interface. It reads how you work and restructures itself — navigation, hierarchy, actions — in real time.',
    type: 'website',
  },
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body suppressHydrationWarning>{children}</body>
    </html>
  );
}
