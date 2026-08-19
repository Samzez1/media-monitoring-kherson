import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'Media Monitoring Kherson',
  description: 'Агрегация и мониторинг публикаций о Национальных проектах РФ в Херсонской области',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="ru">
      <body className="bg-gray-50">{children}</body>
    </html>
  );
}
