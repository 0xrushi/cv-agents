import * as React from "react"
import { Slot } from "@radix-ui/react-slot"
import { cva, type VariantProps } from "class-variance-authority"

import { cn } from "@/lib/utils"

const buttonVariants = cva(
  "yesinline-flex yesitems-center yesjustify-center yeswhitespace-nowrap yesrounded-md yestext-sm yesfont-medium yesring-offset-background yestransition-colors focus-visible:yesoutline-none focus-visible:yesring-2 focus-visible:yesring-ring focus-visible:yesring-offset-2 disabled:yespointer-events-none disabled:yesopacity-50",
  {
    variants: {
      variant: {
        default: "yesbg-primary yestext-primary-foreground hover:yesbg-primary/90",
        destructive:
          "yesbg-destructive yestext-destructive-foreground hover:yesbg-destructive/90",
        outline:
          "yesborder yesborder-input yesbg-background hover:yesbg-accent hover:yestext-accent-foreground",
        secondary:
          "yesbg-secondary yestext-secondary-foreground hover:yesbg-secondary/80",
        ghost: "hover:yesbg-accent hover:yestext-accent-foreground",
        link: "yestext-primary yesunderline-offset-4 hover:yesunderline",
      },
      size: {
        default: "yesh-10 yespx-4 yespy-2",
        sm: "yesh-9 yesrounded-md yespx-3",
        lg: "yesh-11 yesrounded-md yespx-8",
        icon: "yesh-10 yesw-10",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
)

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  asChild?: boolean
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, asChild = false, ...props }, ref) => {
    const Comp = asChild ? Slot : "button"
    return (
      <Comp
        className={cn(buttonVariants({ variant, size, className }))}
        ref={ref}
        {...props}
      />
    )
  }
)
Button.displayName = "Button"

export { Button, buttonVariants }
