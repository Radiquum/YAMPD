"use client";

import { PACK_ENDPOINT, PACKS_ENDPOINT } from "@/api/ENDPOINTS";
import { Pack } from "@/types/pack";
import { Card, Spinner } from "flowbite-react";
import Link from "next/link";
import { useEffect, useState } from "react";

export default function Home() {
  const [packsData, setPacksData] = useState<Pack[]>([]);
  const [packsDataLoading, setPacksDataLoading] = useState(true);

  useEffect(() => {
    async function _getPacksData() {
      const res = await fetch(PACKS_ENDPOINT("getPacks"));
      setPacksData(await res.json());
      setPacksDataLoading(false);
    }
    _getPacksData();
  }, []);

  return (
    <div>
      {packsDataLoading && (
        <div className="w-full flex justify-center items-center">
          <Spinner></Spinner>
        </div>
      )}
      {!packsDataLoading && (
        <div className="grid grid-cols-1 lg:grid-cols-2 2xl:grid-cols-3 gap-2">
          {packsData.map((pack) => {
            return (
              <Link key={pack._id} href={`/pack/?id=${pack._id}`}>
                <Card>
                  <div className="flex gap-2 items-center">
                    {/* eslint-disable-next-line @next/next/no-img-element */}
                    <img
                      alt=""
                      src={PACK_ENDPOINT("getPackImage", pack._id)}
                      className="w-12 h-12 rounded-md"
                    />
                    <div>
                      <p className="text-xl font-semibold">{pack.title}</p>
                      <p className="text-sm text-gray-400">by {pack.author}</p>
                    </div>
                  </div>
                  <div className="flex gap-2 items-center">
                    <p className="text-lg">{pack.modloader}</p>
                    <p className="text-lg">{pack.version}</p>
                    <span> | </span>
                    <p>{pack.mods.length} mods</p>
                  </div>
                </Card>
              </Link>
            );
          })}
        </div>
      )}
    </div>
  );
}
