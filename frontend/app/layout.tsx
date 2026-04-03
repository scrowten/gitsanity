import type { Metadata } from "next";
import { Geist } from "next/font/google";
import "./globals.css";
import { QueryProvider } from "@/components/QueryProvider";

const geist = Geist({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "GitSanity — Discover GitHub repos you'll actually use",
  description: "Personalized GitHub repository discovery based on your interests.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={`${geist.className} bg-gray-50 antialiased`}>
        <QueryProvider>{children}</QueryProvider>
      </body>
    </html>
  );
}
