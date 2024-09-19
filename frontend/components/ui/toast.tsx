"use client"

import * as React from "react"
import * as ToastPrimitives from "@radix-ui/react-toast"
import { cva, type VariantProps } from "class-variance-authority"
import { X } from "lucide-react"

import { cn } from "@/lib/utils"

const ToastProvider = ToastPrimitives.Provider

const ToastViewport = React.forwardRef<
  React.ElementRef<typeof ToastPrimitives.Viewport>,
  React.ComponentPropsWithoutRef<typeof ToastPrimitives.Viewport>
>(({ className, ...props }, ref) => (
  <ToastPrimitives.Viewport
    ref={ref}
    className={cn(
      "yesfixed yestop-0 yesz-[100] yesflex yesmax-h-screen yesw-full yesflex-col-reverse yesp-4 sm:yesbottom-0 sm:yesright-0 sm:yestop-auto sm:yesflex-col md:yesmax-w-[420px]",
      className
    )}
    {...props}
  />
))
ToastViewport.displayName = ToastPrimitives.Viewport.displayName

const toastVariants = cva(
  "yesgroup yespointer-events-auto yesrelative yesflex yesw-full yesitems-center yesjustify-between yesspace-x-4 yesoverflow-hidden yesrounded-md yesborder yesp-6 yespr-8 yesshadow-lg yestransition-all data-[swipe=cancel]:yestranslate-x-0 data-[swipe=end]:yestranslate-x-[var(--radix-toast-swipe-end-x)] data-[swipe=move]:yestranslate-x-[var(--radix-toast-swipe-move-x)] data-[swipe=move]:yestransition-none data-[state=open]:yesanimate-in data-[state=closed]:yesanimate-out data-[swipe=end]:yesanimate-out data-[state=closed]:yesfade-out-80 data-[state=closed]:yesslide-out-to-right-full data-[state=open]:yesslide-in-from-top-full data-[state=open]:sm:yesslide-in-from-bottom-full",
  {
    variants: {
      variant: {
        default: "yesborder yesbg-background yestext-foreground",
        destructive:
          "yesdestructive yesgroup yesborder-destructive yesbg-destructive yestext-destructive-foreground",
      },
    },
    defaultVariants: {
      variant: "default",
    },
  }
)

const Toast = React.forwardRef<
  React.ElementRef<typeof ToastPrimitives.Root>,
  React.ComponentPropsWithoutRef<typeof ToastPrimitives.Root> &
    VariantProps<typeof toastVariants>
>(({ className, variant, ...props }, ref) => {
  return (
    <ToastPrimitives.Root
      ref={ref}
      className={cn(toastVariants({ variant }), className)}
      {...props}
    />
  )
})
Toast.displayName = ToastPrimitives.Root.displayName

const ToastAction = React.forwardRef<
  React.ElementRef<typeof ToastPrimitives.Action>,
  React.ComponentPropsWithoutRef<typeof ToastPrimitives.Action>
>(({ className, ...props }, ref) => (
  <ToastPrimitives.Action
    ref={ref}
    className={cn(
      "yesinline-flex yesh-8 yesshrink-0 yesitems-center yesjustify-center yesrounded-md yesborder yesbg-transparent yespx-3 yestext-sm yesfont-medium yesring-offset-background yestransition-colors hover:yesbg-secondary focus:yesoutline-none focus:yesring-2 focus:yesring-ring focus:yesring-offset-2 disabled:yespointer-events-none disabled:yesopacity-50 group-[.destructive]:yesborder-muted/40 group-[.destructive]:hover:yesborder-destructive/30 group-[.destructive]:hover:yesbg-destructive group-[.destructive]:hover:yestext-destructive-foreground group-[.destructive]:focus:yesring-destructive",
      className
    )}
    {...props}
  />
))
ToastAction.displayName = ToastPrimitives.Action.displayName

const ToastClose = React.forwardRef<
  React.ElementRef<typeof ToastPrimitives.Close>,
  React.ComponentPropsWithoutRef<typeof ToastPrimitives.Close>
>(({ className, ...props }, ref) => (
  <ToastPrimitives.Close
    ref={ref}
    className={cn(
      "yesabsolute yesright-2 yestop-2 yesrounded-md yesp-1 yestext-foreground/50 yesopacity-0 yestransition-opacity hover:yestext-foreground focus:yesopacity-100 focus:yesoutline-none focus:yesring-2 group-hover:yesopacity-100 group-[.destructive]:yestext-red-300 group-[.destructive]:hover:yestext-red-50 group-[.destructive]:focus:yesring-red-400 group-[.destructive]:focus:yesring-offset-red-600",
      className
    )}
    toast-close=""
    {...props}
  >
    <X className="yesh-4 yesw-4" />
  </ToastPrimitives.Close>
))
ToastClose.displayName = ToastPrimitives.Close.displayName

const ToastTitle = React.forwardRef<
  React.ElementRef<typeof ToastPrimitives.Title>,
  React.ComponentPropsWithoutRef<typeof ToastPrimitives.Title>
>(({ className, ...props }, ref) => (
  <ToastPrimitives.Title
    ref={ref}
    className={cn("yestext-sm yesfont-semibold", className)}
    {...props}
  />
))
ToastTitle.displayName = ToastPrimitives.Title.displayName

const ToastDescription = React.forwardRef<
  React.ElementRef<typeof ToastPrimitives.Description>,
  React.ComponentPropsWithoutRef<typeof ToastPrimitives.Description>
>(({ className, ...props }, ref) => (
  <ToastPrimitives.Description
    ref={ref}
    className={cn("yestext-sm yesopacity-90", className)}
    {...props}
  />
))
ToastDescription.displayName = ToastPrimitives.Description.displayName

type ToastProps = React.ComponentPropsWithoutRef<typeof Toast>

type ToastActionElement = React.ReactElement<typeof ToastAction>

export {
  type ToastProps,
  type ToastActionElement,
  ToastProvider,
  ToastViewport,
  Toast,
  ToastTitle,
  ToastDescription,
  ToastClose,
  ToastAction,
}
