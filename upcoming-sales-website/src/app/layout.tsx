import React from "react";
import { Metadata } from 'next';

export const metadata: Metadata = {
    title: "Upcoming MapleStory Cash Shop Sales",
    description: "A tool to see upcoming items going on sale in MapleStory's cash shop!",

}

export default function RootLayout({
    children,
}: {
    children: React.ReactNode
}) {
    return (
        <html lang="en">
            <body>
                <div id="root">{children}</div>
            </body>
        </html>
    )
}