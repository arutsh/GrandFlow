export function Card({
  children,
  className,
}: {
  children: any;
  className?: string | undefined;
}) {
  return (
    <div className={className ?? "w-full bg-slate-500 text-white p-6 mx-10"}>
      {children}
    </div>
  );
}

export function CardHeader({
  children,
  className,
}: {
  children: any;
  className?: string | undefined;
}) {
  return <div className={className ?? ""}>{children}</div>;
}

export function CardContent({
  children,
  className,
}: {
  children: any;
  className?: string | undefined;
}) {
  return <div className={className ?? ""}>{children}</div>;
}
