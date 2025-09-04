import './globals.css';

export const metadata = {
  title: 'Chirality Framework',
  description: '11-Station Semantic Valley Traversal'
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}