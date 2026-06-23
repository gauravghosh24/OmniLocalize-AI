import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "OmniLocalize AI",
  description: "Multilingual Translation and Regional Voice Generation Studio",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
