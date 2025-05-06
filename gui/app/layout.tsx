import type { Metadata } from "next";
import "./globals.css";
import { App } from "./App";

export const metadata: Metadata = {
  title: "YAMPD",
  description: "Yet Another (MineCraft) Mod Pack Downloader",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <App>{children}</App>
    </html>
  );
}
