"use client";

import { Card, FileInput } from "flowbite-react";
import { Label, TextInput, Select } from "flowbite-react";
import { useState } from "react";
import { HiUser, HiAnnotation } from "react-icons/hi";
import { Button } from "flowbite-react";

import mc from "../../../api/mc_version.json";
import { PACKS_ENDPOINT, PACK_ENDPOINT } from "@/api/ENDPOINTS";
import { toast } from "react-toastify";
const mcr = mc.reverse();

export default function PackNew() {
  const [image, setImage] = useState<null | string>(null);
  const [imageMime, setImageMime] = useState<null | string>(null);
  const [packInfo, setPackInfo] = useState({
    title: "",
    author: "",
    modloader: "Forge",
    version: "1.21.5",
  });

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const handleImagePreview = (e: any) => {
    const file = e.target.files[0];
    const fileReader = new FileReader();
    fileReader.onloadend = () => {
      const content = fileReader.result;
      setImage(content as string);
      setImageMime(file.type);
      e.target.value = "";
    };
    fileReader.readAsDataURL(file);
  };

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  function handleInput(e: any) {
    const regex = /[^a-zA-Zа-яА-Я0-9_.()\- \[\]]/g;
    setPackInfo({
      ...packInfo,
      [e.target.name]: e.target.value.replace(regex, ""),
    });
  }

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  function submit(e: any) {
    e.preventDefault();

    async function _submit() {
      const tid = toast.loading(`Creating Pack "${packInfo.title}"`);

      const res = await fetch(PACKS_ENDPOINT("createPack"), {
        method: "POST",
        body: JSON.stringify(packInfo),
        headers: {
          "content-type": "application/json",
          accept: "application/json",
        },
      });
      const data = await res.json();

      if (data.status != "ok") {
        toast.update(tid, {
          render: data.message,
          type: "error",
          isLoading: false,
          autoClose: 2500,
          closeOnClick: true,
          draggable: true,
        });
        return;
      }

      if (image) {
        await fetch(`${PACK_ENDPOINT("editPackImage", data.id)}`, {
          method: "POST",
          body: JSON.stringify({
            image: image,
            mimetype: imageMime,
          }),
          headers: {
            "content-type": "application/json",
            accept: "application/json",
          },
        });
      }

      const ur = new URL(window.location.href);
      ur.searchParams.set("id", data.id);
      ur.pathname = "/pack";
      window.location.href = ur.href;
    }

    _submit();
  }

  return (
    <Card className="w-full">
      <form
        className="flex flex-col gap-4"
        encType="multipart/form-data"
        onSubmit={(e) => submit(e)}
      >
        <div className="flex w-full items-center justify-center">
          <Label
            htmlFor="dropzone-file"
            className="flex h-64 w-full cursor-pointer flex-col items-center justify-center rounded-lg border-2 border-dashed border-gray-300 bg-gray-50 hover:bg-gray-100 dark:border-gray-600 dark:bg-gray-700 dark:hover:border-gray-500 dark:hover:bg-gray-600"
          >
            {image ? (
              // eslint-disable-next-line @next/next/no-img-element
              <img src={image} alt="preview" className="overflow-hidden" />
            ) : (
              <div className="flex flex-col items-center justify-center pb-6 pt-5">
                <svg
                  className="mb-4 h-8 w-8 text-gray-500 dark:text-gray-400"
                  aria-hidden="true"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 20 16"
                >
                  <path
                    stroke="currentColor"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth="2"
                    d="M13 13h3a3 3 0 0 0 0-6h-.025A5.56 5.56 0 0 0 16 6.5 5.5 5.5 0 0 0 5.207 5.021C5.137 5.017 5.071 5 5 5a4 4 0 0 0 0 8h2.167M10 15V6m0 0L8 8m2-2 2 2"
                  />
                </svg>
                <p className="mb-2 text-sm text-gray-500 dark:text-gray-400">
                  <span className="font-semibold">Click to upload</span> or drag
                  and drop
                </p>
                <p className="text-xs text-gray-500 dark:text-gray-400">
                  PNG or JPG
                </p>
              </div>
            )}
            <FileInput
              id="dropzone-file"
              className="hidden"
              name="image"
              onChange={(e) => handleImagePreview(e)}
            />
          </Label>
        </div>
        <div className="flex gap-4">
          <div className="flex-1">
            <div className="mb-2 block">
              <Label htmlFor="base" className="text-lg">
                Title
              </Label>
            </div>
            <TextInput
              id="base"
              type="text"
              sizing="md"
              name="title"
              onChange={(e) => handleInput(e)}
              value={packInfo.title}
              icon={HiAnnotation}
              required
            />
          </div>
          <div className="flex-1">
            <div className="mb-2 block">
              <Label htmlFor="base" className="text-lg">
                Author
              </Label>
            </div>
            <TextInput
              id="base"
              type="text"
              sizing="md"
              name="author"
              onChange={(e) => handleInput(e)}
              value={packInfo.author}
              icon={HiUser}
              required
            />
          </div>
        </div>
        <div className="flex gap-4">
          <div className="flex-1">
            <div className="mb-2 block">
              <Label htmlFor="base" className="text-lg">
                Mod Loader
              </Label>
            </div>
            <Select
              id="modloader"
              name="modloader"
              required
              onChange={(e) => handleInput(e)}
            >
              <option value="Forge">Forge</option>
              <option value="Fabric">Fabric</option>
              <option value="NeoForge">NeoForge</option>
              <option value="Quilt">Quilt</option>
            </Select>
          </div>
          <div className="flex-1">
            <div className="mb-2 block">
              <Label htmlFor="base" className="text-lg">
                Game Version
              </Label>
            </div>
            <Select
              id="version"
              name="version"
              required
              onChange={(e) => handleInput(e)}
            >
              {mcr.map((version) => (
                <option key={version} value={version}>
                  {version}
                </option>
              ))}
            </Select>
          </div>
        </div>
        <div className="flex justify-end">
          <Button type="submit">Create</Button>
        </div>
      </form>
    </Card>
  );
}
