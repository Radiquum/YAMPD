"use client";

import { MOD_ENDPOINT, PACK_ENDPOINT, PACKS_ENDPOINT } from "@/api/ENDPOINTS";
import { Pack } from "@/types/pack";
import {
  Button,
  Card,
  Label,
  Select,
  Spinner,
  TextInput,
} from "flowbite-react";
import { useSearchParams } from "next/navigation";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { Modal, ModalBody, ModalFooter, ModalHeader } from "flowbite-react";

import { HiDownload, HiPlusCircle, HiTrash } from "react-icons/hi";
import { ModTable } from "../components/ModTable";
import { toast } from "react-toastify";

export default function PackPage() {
  const [packData, setPackData] = useState<Pack | null>(null);
  const [packDataLoading, setPackDataLoading] = useState(true);
  const router = useRouter();
  const id = useSearchParams().get("id") || "";

  const [addModModalOpen, setAddModModalOpen] = useState(true);
  const [modSource, setModSource] = useState<"Modrinth" | "CurseForge">(
    "Modrinth"
  );
  const [modUrl, setModUrl] = useState({
    placeholer: "https://modrinth.com/mod/{ slug }</version/{ file_id }>",
    value: "",
  });
  // const [modParams, setModParams] = useState<{
  //   slug: string;
  //   version: string | null;
  // }>({
  //   slug: "",
  //   version: null,
  // });

  async function _getPacksData() {
    const res = await fetch(PACK_ENDPOINT("getPack", id));
    if (!res.ok) router.push("/404");
    const data: Pack = await res.json();
    setPackData(data);
    setPackDataLoading(false);
  }

  useEffect(() => {
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
      const ur = new URL(window.location.href);
      ur.searchParams.delete("id");
      ur.pathname = "/";
      window.location.href = ur.href;
    }
  }

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const handleModSource = (e: any) => {
    switch (e.target.value) {
      case "Modrinth":
        setModSource("Modrinth");
        setModUrl({
          placeholer: "https://modrinth.com/mod/{ slug }</version/{ file_id }>",
          value: "",
        });
        break;
      case "CurseForge":
        setModSource("CurseForge");
        setModUrl({
          placeholer:
            "https://www.curseforge.com/minecraft/mc-mods/{ slug }</files/{ file_id }>",
          value: "",
        });
        break;
    }
  };

  async function addMod() {
    let slug = null;
    let version = null;

    if (!modUrl.value) {
      toast.error("Mod url is required", {
        autoClose: 2500,
        closeOnClick: true,
        draggable: true,
      });
      return;
    }

    switch (modSource) {
      case "Modrinth":
        const _tmp = modUrl.value.split("/mod/");
        if (_tmp.length == 1) {
          toast.error("invalid Modrinth url", {
            autoClose: 2500,
            closeOnClick: true,
            draggable: true,
          });
          return;
        }
        const _tmp2 = _tmp[1].split("/version/");
        slug = _tmp2[0];
        if (_tmp2.length > 1) {
          version = _tmp2[1];
        }
        break;
      case "CurseForge":
        const _tmp3 = modUrl.value.split("/mc-mods/");
        if (_tmp3.length == 1) {
          toast.error("invalid CurseForge url", {
            autoClose: 2500,
            closeOnClick: true,
            draggable: true,
          });
          return;
        }
        const _tmp4 = _tmp3[1].split("/files/");
        slug = _tmp4[0];
        if (_tmp4.length > 1) {
          version = _tmp4[1];
        }
        break;
    }

    slug = slug.replace("/", "");
    version = version ? version.replace("/", "") : null;

    // if (packMods.find((elem) => elem.slug == slug)) {
    //   toast.error(`mod (${slug}) already exists`, {
    //     autoClose: 2500,
    //     closeOnClick: true,
    //     draggable: true,
    //   });
    //   return;
    // }

    if (!packData) return;
    const tid = toast.loading(`Adding mod`);
    const res = await fetch(MOD_ENDPOINT("addMod", packData._id), {
      method: "POST",
      body: JSON.stringify({
        slug,
        version,
        source: modSource,
      }),
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

    toast.update(tid, {
      render: data.message,
      type: "success",
      isLoading: false,
      autoClose: 2500,
      closeOnClick: true,
      draggable: true,
    });
    setModUrl({ ...modUrl, value: "" });

    _getPacksData();
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
          <Card className="sticky top-0 left-0 right-0 z-10">
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
              <div className="flex gap-2 items-center">
                <div>
                  <p className="text-lg font-semibold">
                    {packData.mods.length} mods
                  </p>
                  <p className="text-sm text-gray-400">
                    v{packData.modpackVersion}
                  </p>
                </div>
                <Button onClick={() => setAddModModalOpen(true)}>
                  Add mod <HiPlusCircle className="ml-2 h-5 w-5" />
                </Button>
                <Button>
                  Download <HiDownload className="ml-2 h-5 w-5" />
                </Button>
                <Button color={"red"} onClick={() => deletePack()}>
                  Delete <HiTrash className="ml-2 h-5 w-5" />
                </Button>
              </div>
            </div>
          </Card>
          <div className="mt-4">
            <ModTable mods={packData.mods} updatePack={_getPacksData} packID={id} />
          </div>
        </div>
      )}
      <Modal
        dismissible
        show={addModModalOpen}
        onClose={() => setAddModModalOpen(false)}
      >
        <ModalHeader>Terms of Service</ModalHeader>
        <ModalBody>
          <div className="space-y-6">
            <div className="flex-1">
              <div className="mb-2 block">
                <Label htmlFor="base" className="text-lg">
                  Source
                </Label>
              </div>
              <Select
                id="source"
                name="source"
                required
                onChange={(e) => handleModSource(e)}
              >
                <option value="Modrinth">Modrinth</option>
                <option value="CurseForge">CurseForge</option>
              </Select>
            </div>
            <div className="flex-1">
              <div className="mb-2 block">
                <Label htmlFor="base" className="text-lg">
                  Link
                </Label>
              </div>
              <TextInput
                id="base"
                type="text"
                sizing="md"
                name="author"
                onChange={(e) =>
                  setModUrl({ ...modUrl, value: e.target.value })
                }
                value={modUrl.value}
                placeholder={modUrl.placeholer}
                required
              />
            </div>
          </div>
        </ModalBody>
        <ModalFooter>
          <Button onClick={() => addMod()}>Save</Button>
        </ModalFooter>
      </Modal>
    </div>
  );
}
