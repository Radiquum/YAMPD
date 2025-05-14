import { MOD_ENDPOINT } from "@/api/ENDPOINTS";
import { Mod } from "@/types/mod";
import { Button } from "flowbite-react";
import { useState } from "react";
import { HiDownload, HiTrash } from "react-icons/hi";
import { toast } from "react-toastify";
import {
  Accordion,
  AccordionContent,
  AccordionPanel,
  AccordionTitle,
} from "flowbite-react";

export const ModTable = (props: {
  mods: Mod[];
  updatePack: () => void;
  packID: string;
  downloadMods: (mods: string[]) => void;
}) => {
  function bytesToSize(bytes) {
    var sizes = ["Bytes", "KB", "MB", "GB", "TB"];
    if (bytes == 0) return "n/a";
    var i = parseInt(Math.floor(Math.log(bytes) / Math.log(1024)));
    if (i == 0) return bytes + " " + sizes[i];
    return (bytes / Math.pow(1024, i)).toFixed(1) + " " + sizes[i];
  }

  async function deleteMod(slug: string, title: string) {
    if (!window) return;
    if (window.confirm(`Delete mod ${title}?`)) {
      const res = await fetch(MOD_ENDPOINT("deleteMod", props.packID, slug));
      const data = await res.json();

      if (data.status != "ok") {
        toast.error(data.message, {
          autoClose: 2500,
          closeOnClick: true,
          draggable: true,
        });
        return;
      }

      props.updatePack();
    }
  }

  if (!props.mods || props.mods.length == 0) {
    return <></>;
  }

  return (
    <Accordion>
      {props.mods.map((mod) => {
        return (
          <AccordionPanel key={`mod-${mod.slug}`}>
            <AccordionTitle>
              <div className="flex gap-2 items-center text-2xl">
                <img alt="" src={mod.icon} className="w-8 h-8 rounded-lg" />
                {mod.title} ({mod.slug})
              </div>
            </AccordionTitle>
            <AccordionContent>
              <div className="flex gap-8 flex-wrap">
                <div className="flex gap-2 flex-col">
                  <div>
                    <p className="font-semibold text-xl">Developers</p>
                    {mod.developers.join(", ")}
                  </div>
                  <div>
                    <p className="font-semibold text-xl">Source</p>
                    <p>
                      <span className="font-semibold">title:</span> {mod.source}
                    </p>
                    <p>
                      <span className="font-semibold">id:</span>{" "}
                      {mod.project_id}
                    </p>
                    <p>
                      <span className="font-semibold">link:</span> {mod.url}
                    </p>
                  </div>
                </div>
                <div>
                  <p className="font-semibold text-xl">Version info</p>
                  <p>
                    <span className="font-semibold">filename:</span>{" "}
                    {mod.file.filename}
                  </p>
                  <p>
                    <span className="font-semibold">version:</span>{" "}
                    {mod.file.version}
                  </p>
                  <p>
                    <span className="font-semibold">file size:</span>{" "}
                    {bytesToSize(mod.file.size)}
                  </p>
                </div>
                <div>
                  <p className="font-semibold text-xl">Environment</p>
                  {mod.environment.client && <p>client</p>}
                  {mod.environment.server && <p>server</p>}
                  {mod.environment.client && mod.environment.server && (
                    <p>client & server</p>
                  )}
                  {/* <p>
                    <span className="font-semibold">filename:</span>{" "}
                    {mod.file.filename}
                  </p>
                  <p>
                    <span className="font-semibold">version:</span>{" "}
                    {mod.file.version}
                  </p>
                  <p>
                    <span className="font-semibold">file size:</span>{" "}
                    {bytesToSize(mod.file.size)}
                  </p> */}
                </div>
              </div>
              <div className="mt-2">
                <p className="font-semibold text-xl">Hashes</p>
                {Object.entries(mod.file.hashes).map((hash) => {
                  return (
                    <p
                      key={`mod-${mod.slug}-hash-${hash[0]}`}
                      className="wrap-break-word"
                    >
                      <span className="font-semibold">{hash[0]}:</span>{" "}
                      {hash[1]}
                    </p>
                  );
                })}
              </div>
              {mod.dependencies.length > 0 ? (
                <div className="mt-2">
                  <p className="font-semibold text-xl mb-1">Dependencies</p>
                  <div className="flex gap-2 overflow-x-auto overflow-y-hidden">
                    {mod.dependencies.map((dep) => {
                      return (
                        <div
                          key={`mod-${mod.slug}-dep-${dep.slug}`}
                          className="bg-[#f3f4f6] dark:bg-[#1f2937] p-4 rounded-lg"
                        >
                          <div className="flex gap-2 items-center text-xl">
                            <img
                              alt=""
                              src={dep.icon}
                              className="w-6 h-6 rounded-lg"
                            />
                            {dep.title} ({dep.slug})
                          </div>
                          <div className="mt-1">
                            <p>
                              <span className="font-semibold">filename:</span>{" "}
                              {dep.file.filename}
                            </p>
                            <p>
                              <span className="font-semibold">version:</span>{" "}
                              {dep.file.version}
                            </p>
                            <p>
                              <span className="font-semibold">file size:</span>{" "}
                              {bytesToSize(dep.file.size)}
                            </p>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </div>
              ) : (
                ""
              )}
              <div className="flex justify-end w-full gap-2 mt-4">
                <Button
                  size="sm"
                  onClick={() => props.downloadMods([mod.slug])}
                >
                  Download <HiDownload className="ml-2 h-4 w-4" />
                </Button>
                <Button
                  color={"red"}
                  size="sm"
                  onClick={() => deleteMod(mod.slug, mod.title)}
                >
                  Delete <HiTrash className="ml-2 h-4 w-4" />
                </Button>
              </div>
            </AccordionContent>
          </AccordionPanel>
        );
      })}
    </Accordion>
  );
};
