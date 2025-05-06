import { MOD_ENDPOINT } from "@/api/ENDPOINTS";
import { Mod } from "@/types/mod";
import {
  Button,
  Checkbox,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeadCell,
  TableRow,
} from "flowbite-react";
import { useState } from "react";
import { HiDownload, HiTrash } from "react-icons/hi";
import { toast } from "react-toastify";

export const ModTable = (props: {
  mods: Mod[];
  updatePack: () => void;
  packID: string;
}) => {
  const [selectedMods, setSelectedMods] = useState<string[]>([]);

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

  function selectAll() {
    const deselect = selectedMods.length == props.mods.length;
    console.log(selectedMods.length, props.mods.length, deselect);
    if (deselect) {
      setSelectedMods([]);
      return;
    }
    props.mods.forEach((item) => {
      if (!selectedMods.includes(item.slug)) {
        setSelectedMods((state) => [item.slug, ...state]);
      }
    });
  }

  function handleCheckbox(slug: string) {
    if (!selectedMods.includes(slug)) {
      setSelectedMods((state) => [slug, ...state]);
    } else {
      const newArray = selectedMods.map((i) => i);
      const idx = newArray.findIndex((item) => item == slug);
      newArray.splice(idx, 1);
      setSelectedMods(newArray);
    }
  }

  async function deleteSelectedMods() {
    await fetch(MOD_ENDPOINT("deleteModBulk", props.packID), {
      method: "POST",
      body: JSON.stringify(selectedMods),
      headers: {
        "content-type": "application/json",
        accept: "application/json",
      },
    });
    setSelectedMods([]);
    props.updatePack();
  }

  return (
    <div className="overflow-x-auto">
      <Table hoverable>
        <TableHead>
          <TableRow>
            <TableHeadCell className="p-4">
              <Checkbox
                checked={selectedMods.length == props.mods.length}
                onChange={() => selectAll()}
              />
            </TableHeadCell>
            <TableHeadCell>Icon</TableHeadCell>
            <TableHeadCell>Title</TableHeadCell>
            <TableHeadCell>Version</TableHeadCell>
            <TableHeadCell>Developer</TableHeadCell>
            <TableHeadCell>Source</TableHeadCell>
            <TableHeadCell>Source URL</TableHeadCell>
            <TableHeadCell>
              <span className="sr-only">Actions</span>
            </TableHeadCell>
          </TableRow>
        </TableHead>
        <TableBody className="divide-y">
          {props.mods &&
            props.mods.length > 0 &&
            props.mods.map((mod) => {
              return (
                <TableRow
                  key={`mod-${mod.slug}`}
                  className="bg-white dark:border-gray-700 dark:bg-gray-800"
                >
                  <TableCell className="p-4">
                    <Checkbox
                      checked={selectedMods.includes(mod.slug)}
                      onChange={() => {
                        handleCheckbox(mod.slug);
                      }}
                    />
                  </TableCell>
                  <TableCell>
                    {/* eslint-disable-next-line @next/next/no-img-element */}
                    <img alt="" src={mod.icon} className="w-8 h-8 rounded-lg" />
                  </TableCell>
                  <TableCell className="whitespace-nowrap font-medium text-gray-900 dark:text-white">
                    {mod.title}
                  </TableCell>
                  <TableCell>{mod.file.version}</TableCell>
                  <TableCell>{mod.developers.join(", ")}</TableCell>
                  <TableCell>{mod.source}</TableCell>
                  <TableCell>{mod.url}</TableCell>
                  <TableCell>
                    <div className="flex gap-2">
                      <Button size="sm">
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
                  </TableCell>
                </TableRow>
              );
            })}
          <TableRow className="bg-white dark:bg-[#374151] hover:bg-white! hover:dark:bg-[#374151]! dark:border-gray-700">
            <TableCell className="p-4"></TableCell>
            <TableCell></TableCell>
            <TableCell></TableCell>
            <TableCell></TableCell>
            <TableCell></TableCell>
            <TableCell></TableCell>
            <TableCell></TableCell>
            <TableCell>
              <Button
                color={"red"}
                size="sm"
                disabled={selectedMods.length == 0}
                onClick={() => deleteSelectedMods()}
              >
                Delete Selected <HiTrash className="ml-2 h-4 w-4" />
              </Button>
            </TableCell>
          </TableRow>
        </TableBody>
      </Table>
    </div>
  );
};
