"use client";

import { PACK_ENDPOINT, PACKS_ENDPOINT } from "@/api/ENDPOINTS";
import { Pack } from "@/types/pack";
import { Button, Card, Spinner } from "flowbite-react";
import { useSearchParams } from "next/navigation";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

import { HiDownload, HiTrash } from "react-icons/hi";

export default function PackPage() {
  const [packData, setPackData] = useState<Pack | null>(null);
  const [packDataLoading, setPackDataLoading] = useState(true);
  const router = useRouter();
  const id = useSearchParams().get("id") || "";

  useEffect(() => {
    async function _getPacksData() {
      const res = await fetch(PACK_ENDPOINT("getPack", id));
      if (!res.ok) router.push("/404");
      setPackData(await res.json());
      setPackDataLoading(false);
    }
    if (id) {
      _getPacksData();
    } else {
      router.push("/404");
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const handleImageUpdate = (e: any) => {
    if (!packData || !window) return;

    const file = e.target.files[0];
    const fileReader = new FileReader();
    fileReader.onloadend = () => {
      const content = fileReader.result;
      fetch(`${PACK_ENDPOINT("editPackImage", packData._id)}`, {
        method: "POST",
        body: JSON.stringify({
          image: content,
          mimetype: file.type,
        }),
        headers: {
          "content-type": "application/json",
          accept: "application/json",
        },
      }).then(() => location.reload());
      e.target.value = "";
    };
    fileReader.readAsDataURL(file);
  };

  function deletePack() {
    if (!packData || !window) return;

    if (window.confirm(`Delete pack ${packData.title}?`)) {
      fetch(`${PACKS_ENDPOINT("deletePack", packData._id)}`);
      const ur = new URL(window.location.href)
      ur.searchParams.delete("id")
      ur.pathname = "/"
      window.location.href = ur.href
    }
  }

  return (
    <div>
      {packDataLoading && (
        <div className="w-full flex justify-center items-center">
          <Spinner></Spinner>
        </div>
      )}
      {packData && (
        <div>
          <Card className="sticky top-0 left-0 right-0">
            <div className="flex gap-4 items-center justify-between">
              <div>
                <p className="text-xl font-semibold">{packData.version}</p>
                <p className="text-sm text-gray-400">{packData.modloader}</p>
              </div>
              <div className="flex gap-2 items-center">
                <label htmlFor="pack-icon" className="cursor-pointer">
                  {/* eslint-disable-next-line @next/next/no-img-element */}
                  <img
                    alt=""
                    src={PACK_ENDPOINT("getPackImage", packData._id)}
                    className="w-12 h-12 rounded-md"
                  />
                </label>
                <input
                  onChange={(e) => handleImageUpdate(e)}
                  id="pack-icon"
                  className="hidden"
                  name="image"
                  type="file"
                />
                <div>
                  <p className="text-xl font-semibold">{packData.title}</p>
                  <p className="text-sm text-gray-400">by {packData.author}</p>
                </div>
              </div>
              <div className="flex gap-2">
                <Button color={"red"} onClick={() => deletePack()}>
                  Delete <HiTrash className="ml-2 h-5 w-5" />
                </Button>
                <Button>
                  Download <HiDownload className="ml-2 h-5 w-5" />
                </Button>
              </div>
            </div>
          </Card>
        </div>
      )}
    </div>
  );
}
