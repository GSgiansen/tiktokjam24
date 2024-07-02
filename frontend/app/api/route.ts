export const dynamic = "force-dynamic"; // defaults to auto

export async function POST(request: Request) {
  try {
    const headers = [];
    const formData = await request.formData();
    const file = formData.get("file") as File;
    const buffer = Buffer.from(await file.arrayBuffer());
    console.log(buffer.toString());

    return Response.json({
      headers: buffer.toString().split("\n")[0].split(","),
    });
  } catch (err) {
    console.error(err);
  }
  return Response.json({ message: "ERROR" });
}
