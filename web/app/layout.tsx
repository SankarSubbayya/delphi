import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Delphi",
  description: "Synthetic populations as a computational substrate.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
