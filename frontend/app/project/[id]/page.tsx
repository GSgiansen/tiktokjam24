type MetricsComponentProps = {
  id: string;
};

const MetricsComponent = ({ id: string }: MetricsComponentProps) => {
  return <>show metrics</>;
};

export default function Page({ params }: { params: { id: string } }) {
  return (
    <>
      <MetricsComponent id={params.id} />
    </>
  );
}
