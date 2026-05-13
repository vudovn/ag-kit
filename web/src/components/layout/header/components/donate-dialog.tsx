'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Dialog, DialogClose, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import { CoffeeIcon, Heart, QrCodeIcon } from 'lucide-react';

interface DonateDialogProps {
    className?: string;
}

export default function DonateDialog({ className }: DonateDialogProps) {
    const [showQR, setShowQR] = useState(false);

    return (
        <Dialog>
            <DialogTrigger render={<Button variant="outline" className={className} />}>
                <Heart className="w-3 h-3 mr-1.5 text-red-500" />
                Donate
            </DialogTrigger>
            <DialogContent className="sm:max-w-md">
                <DialogHeader>
                    <DialogTitle className="flex items-center gap-2">
                        <span>Fuel the Developer</span>
                    </DialogTitle>
                    <DialogDescription className="space-y-2 pt-2">
                        Hi! I&apos;m <strong>Vu</strong>. I&apos;m dedicating my full-time work to building this kit. <br />
                        Your support helps me keep shipping and maintaining it. If you find this tool helpful, please consider buying me a coffee.
                    </DialogDescription>
                </DialogHeader>

                <div className="space-y-3 p-4">
                    {/* Buy Me a Coffee */}
                    <a
                        href="https://buymeacoffee.com/vudovn"
                        target="_blank"
                        rel="noopener noreferrer"
                        className="flex items-center gap-3 p-4 rounded-lg border border-zinc-200 dark:border-zinc-800 hover:border-zinc-300 dark:hover:border-zinc-700 hover:bg-zinc-50 dark:hover:bg-zinc-900 transition-all group"
                    >
                        <div className="flex items-center justify-center w-10 h-10 rounded-full bg-amber-100 dark:bg-amber-900/20">
                            <CoffeeIcon className="w-5 h-5 text-amber-600 dark:text-amber-500" />
                        </div>
                        <div className="flex-1">
                            <div className="font-semibold text-zinc-900 dark:text-zinc-50 mb-0.5">Buy Me a Coffee</div>
                            <div className="text-sm text-zinc-600 dark:text-zinc-400">Support via buymeacoffee.com</div>
                        </div>
                        <svg className="w-5 h-5 text-zinc-400 group-hover:text-zinc-600 dark:group-hover:text-zinc-300 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                        </svg>
                    </a>

                    {/* Bank Transfer with QR */}
                    <button
                        onClick={() => setShowQR(!showQR)}
                        className="w-full flex items-center gap-3 p-4 rounded-lg border border-zinc-200 dark:border-zinc-800 hover:border-zinc-300 dark:hover:border-zinc-700 hover:bg-zinc-50 dark:hover:bg-zinc-900 transition-all group text-left"
                    >
                        <div className="flex items-center justify-center w-10 h-10 rounded-full bg-blue-100 dark:bg-blue-900/20">
                            <QrCodeIcon className="w-5 h-5 text-blue-600 dark:text-blue-500" />
                        </div>
                        <div className="flex-1">
                            <div className="font-semibold text-zinc-900 dark:text-zinc-50 mb-0.5">Bank Transfer</div>
                            <div className="text-sm text-zinc-600 dark:text-zinc-400">Direct transfer via QR code</div>
                        </div>
                        <svg className={`w-5 h-5 text-zinc-400 transition-transform ${showQR ? 'rotate-90' : ''}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                        </svg>
                    </button>

                    {/* QR Code Display */}
                    {showQR && (
                        <div className="p-4 rounded-lg border border-zinc-200 dark:border-zinc-800 bg-zinc-50 dark:bg-zinc-900/50">
                            <div className="flex flex-col items-center gap-4">
                                {/* QR Code Placeholder - Replace with actual QR code image */}
                                <img className="w-48 h-48 rounded-lg" src="https://img.vietqr.io/image/mbbank-0779440918-compact.jpg" alt="" />
                                {/* Bank Details */}
                                <div className="text-center space-y-1">
                                    <div className="text-sm font-medium text-zinc-900 dark:text-zinc-50">
                                        Bank: <span className="font-mono">MB Bank</span>
                                    </div>
                                    <div className="text-sm font-medium text-zinc-900 dark:text-zinc-50">
                                        Account: <span className="font-mono">0779440918</span>
                                    </div>
                                    <div className="text-sm font-medium text-zinc-900 dark:text-zinc-50">
                                        Name: <span className="font-mono">DO VAN VU</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    )}

                    {/* Hire Me Option */}
                    {/* <a
                        href="https://www.linkedin.com/in/vudovn" // Assuming this link based on username, user can update
                        target="_blank"
                        rel="noopener noreferrer"
                        className="flex items-center gap-3 p-4 rounded-lg border border-zinc-200 dark:border-zinc-800 hover:border-blue-500/50 dark:hover:border-blue-500/50 hover:bg-blue-50 dark:hover:bg-blue-900/10 transition-all group"
                    >
                        <div className="flex items-center justify-center w-10 h-10 rounded-full bg-indigo-100 dark:bg-indigo-900/20">
                            <span className="text-xl">
                                <User />
                            </span>
                        </div>
                        <div className="flex-1">
                            <div className="font-semibold text-zinc-900 dark:text-zinc-50 mb-0.5">Hire Me!</div>
                            <div className="text-sm text-zinc-600 dark:text-zinc-400">View my profile & portfolio</div>
                        </div>
                        <svg className="w-5 h-5 text-zinc-400 group-hover:text-blue-500 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                        </svg>
                    </a> */}
                </div>

                <DialogFooter>
                    <DialogClose render={<Button variant="ghost" />}>
                        Close
                    </DialogClose>
                </DialogFooter>
            </DialogContent>
        </Dialog>
    );
}
