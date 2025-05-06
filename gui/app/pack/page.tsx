"use client";

import {
  DOWNLOAD_ENDPOINT,
  MOD_ENDPOINT,
  PACK_ENDPOINT,
  PACKS_ENDPOINT,
} from "@/api/ENDPOINTS";
import { Pack } from "@/types/pack";
import {
  Button,
  Card,
  Label,
  Progress,
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

import { io } from "socket.io-client";
const socketURL = process.env.NEXT_PUBLIC_SOCKET_URL
  ? process.env.NEXT_PUBLIC_SOCKET_URL
  : undefined;
const socket = io(socketURL);

export default function PackPage() {
  const [packData, setPackData] = useState<Pack | null>(null);
  const [packDataLoading, setPackDataLoading] = useState(true);
  const router = useRouter();
  const id = useSearchParams().get("id") || "";

  const [addModModalOpen, setAddModModalOpen] = useState(false);
  const [modUrl, setModUrl] = useState("");

  const [downloadModalOpen, setdownloadModalOpen] = useState(false);
  const [downloadProgressFile, setDownloadProgressFile] = useState({
    filename: "filename",
    total: 1,
    current: 1,
  });
  const [downloadProgressTotal, setDownloadProgressTotal] = useState(100);
  const [downloadProgressCurrent, setDownloadProgressCurrent] = useState(100);

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

  useEffect(() => {
    function percentage(partialValue: number, totalValue: number) {
      const flo = (100 * partialValue) / totalValue;
      return Number(flo.toFixed(2));
    }

    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    function onDownloadCurrent(data: any) {
      switch (data.status) {
        case "pending":
          const progress = percentage(data.download_bytes, data.total_bytes);
          setDownloadProgressCurrent(progress);
          break;
        case "ok":
          setDownloadProgressCurrent(0);
          break;
        case "error":
          toast.error(data.message, {
            autoClose: 2500,
            closeOnClick: true,
            draggable: true,
          });
          break;
        default:
          console.log(`GET UNKNOWN WS STATUS: ${data.status}`);
          break;
      }
    }

    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    function onDownloadTotal(data: any) {
      const progress = percentage(data.current, data.total);
      setDownloadProgressTotal(progress);
      setDownloadProgressFile({
        filename: data.filename,
        total: data.total,
        current: data.current,
      });
    }

    socket.on("download_current", (data) => onDownloadCurrent(data));
    socket.on("download_total", (data) => onDownloadTotal(data));

    return () => {
      socket.off("download_current", (data) => onDownloadCurrent(data));
      socket.off("download_total", (data) => onDownloadTotal(data));
    };
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

  async function addMod() {
    let slug = null;
    let version = null;

    if (!modUrl) {
      toast.error("Mod url is required", {
        autoClose: 2500,
        closeOnClick: true,
        draggable: true,
      });
      return;
    }

    let source = null;

    if (modUrl.includes("modrinth.com")) {
      source = "Modrinth";
    } else if (modUrl.includes("curseforge.com")) {
      source = "CurseForge";
    } else {
      toast.error("unknown source", {
        autoClose: 2500,
        closeOnClick: true,
        draggable: true,
      });
      return;
    }

    switch (source) {
      case "Modrinth":
        const _tmp = modUrl.split("/mod/");
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
        const _tmp3 = modUrl.split("/mc-mods/");
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
      default:
        toast.error("failed to parse url", {
          autoClose: 2500,
          closeOnClick: true,
          draggable: true,
        });
        return;
    }

    slug = slug.replace("/", "");
    version = version ? version.replace("/", "") : null;

    if (!packData) return;
    const tid = toast.loading(`Adding mod`);
    const res = await fetch(MOD_ENDPOINT("addMod", packData._id), {
      method: "POST",
      body: JSON.stringify({
        slug,
        version,
        source,
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
    // setModUrl({ ...modUrl, value: "" });

    _getPacksData();
  }

  async function downloadPack() {
    if (!packData) return;

    fetch(`${DOWNLOAD_ENDPOINT["downloadPack"]}`, {
      method: "POST",
      body: JSON.stringify({
        pack_id: packData._id,
      }),
      headers: {
        "content-type": "application/json",
        accept: "application/json",
      },
    });

    setdownloadModalOpen(true);
  }

  async function downloadMods(mods: string[]) {
    if (!packData) return;

    fetch(`${DOWNLOAD_ENDPOINT["downloadMods"]}`, {
      method: "POST",
      body: JSON.stringify({
        pack_id: packData._id,
        mods: mods,
      }),
      headers: {
        "content-type": "application/json",
        accept: "application/json",
      },
    });

    setdownloadModalOpen(true);
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
                <Button onClick={() => downloadPack()}>
                  Download <HiDownload className="ml-2 h-5 w-5" />
                </Button>
                <Button color={"red"} onClick={() => deletePack()}>
                  Delete <HiTrash className="ml-2 h-5 w-5" />
                </Button>
              </div>
            </div>
          </Card>
          <div className="mt-4">
            <ModTable
              mods={packData.mods}
              updatePack={_getPacksData}
              downloadMods={downloadMods}
              packID={id}
            />
          </div>
        </div>
      )}
      <Modal
        dismissible
        show={addModModalOpen}
        onClose={() => setAddModModalOpen(false)}
      >
        <ModalHeader>Add a mod</ModalHeader>
        <ModalBody>
          <div className="space-y-6">
            <div className="flex-1">
              <div className="mb-2 block">
                <Label htmlFor="mod_url" className="text-lg">
                  Link
                </Label>
              </div>
              <TextInput
                id="mod_url"
                type="text"
                sizing="md"
                name="mod_url"
                onChange={(e) => setModUrl(e.target.value)}
                value={modUrl}
                required
              />
              <p className="mt-2 text-gray-400">Can be one of:</p>
              <ul className="text-gray-400 list-disc">
                <li className="ml-4">
                  https://modrinth.com/mod/[slug][/version/file_id]
                </li>
                <li className="ml-4">
                  https://www.curseforge.com/minecraft/mc-mods/[slug][/files/file_id]
                </li>
              </ul>
            </div>
          </div>
        </ModalBody>
        <ModalFooter>
          <Button onClick={() => addMod()}>Save</Button>
        </ModalFooter>
      </Modal>
      <Modal
        show={downloadModalOpen}
        dismissible={downloadProgressFile.current == downloadProgressFile.total}
        onClose={() => {
          if (downloadProgressFile.current == downloadProgressFile.total) {
            setdownloadModalOpen(false);
          }
        }}
      >
        <ModalHeader>Download progress</ModalHeader>
        <ModalBody>
          <div className="mb-4">
            <Progress
              progress={downloadProgressTotal}
              progressLabelPosition="inside"
              textLabel="Total"
              textLabelPosition="outside"
              size="lg"
              labelProgress
              labelText
            />
            <div className="flex justify-end items-center mb-2">
              <p>
                {downloadProgressFile.current} / {downloadProgressFile.total}
              </p>
            </div>
          </div>
          <div>
            <Progress
              progress={downloadProgressCurrent}
              progressLabelPosition="inside"
              textLabel={downloadProgressFile.filename}
              textLabelPosition="outside"
              size="lg"
              labelProgress
              labelText
            />
          </div>
          {downloadProgressFile.current == downloadProgressFile.total ? (
            <p>
              Mods downloaded, You can find them in path: packs/{packData?._id}
              /mods
            </p>
          ) : (
            ""
          )}
        </ModalBody>
        <ModalFooter>
          <Button
            disabled={
              downloadProgressFile.current != downloadProgressFile.total
            }
            onClick={() => setdownloadModalOpen(false)}
          >
            Close
          </Button>
        </ModalFooter>
      </Modal>
    </div>
  );
}
