"use client";

import { PACK_ENDPOINT, PACKS_ENDPOINT } from "@/api/ENDPOINTS";
import { Pack } from "@/types/pack";
import {
  Sidebar,
  SidebarItem,
  SidebarItemGroup,
  SidebarItems,
} from "flowbite-react";
import { useEffect, useState } from "react";
import { HiChartPie, HiPlusCircle } from "react-icons/hi";

export const Menu = () => {
  const [packsData, setPacksData] = useState<Pack[]>([]);
  useEffect(() => {
    async function _getPacksData() {
      const res = await fetch(PACKS_ENDPOINT("getPacks"));
      setPacksData(await res.json());
    }
    _getPacksData();
  }, []);

  return (
    <Sidebar aria-label="Default sidebar example">
      <SidebarItems>
        <SidebarItemGroup>
          <SidebarItem href="/" icon={HiChartPie}>
            Dashboard
          </SidebarItem>
          {packsData &&
            packsData.map((pack) => {
              return (
                <SidebarItem
                  href={`/pack/?id=${pack._id}`}
                  key={pack._id}
                  theme={{
                    content: {
                      base: "p-0!",
                    },
                  }}
                >
                  <div className="flex gap-2 items-center">
                    {/* eslint-disable-next-line @next/next/no-img-element */}
                    <img
                      alt=""
                      src={PACK_ENDPOINT("getPackImage", pack._id)}
                      className="w-10 h-10 rounded-md"
                    />
                    <div>
                      <p className="line-clamp-1">{pack.title}</p>
                      <p className="text-sm text-gray-400 line-clamp-1">
                        by {pack.author}
                      </p>
                    </div>
                  </div>
                </SidebarItem>
              );
            })}
          <SidebarItem href="/pack/new" icon={HiPlusCircle}>
            New mod pack
          </SidebarItem>
        </SidebarItemGroup>
      </SidebarItems>
    </Sidebar>
  );
};
