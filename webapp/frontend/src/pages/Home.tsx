import { Button } from "@/components/ui/button"
import { useEffect, useRef, useState } from "react"
import { BACKEND_URL, local_file } from "@/constant"
import { Download, Edit, Trash2, UploadIcon } from "lucide-react"
import { useNavigate } from "react-router-dom"
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,

} from "@/components/ui/alert-dialog"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
type sketchData={
  id:number,
  name:string
}
function Home() {
    const [data,setData]=useState<sketchData[]>([])
    const [id,setId]=useState<number|null>(null)
    const [open,setOpen]=useState<boolean>(false)
    const [open2,setOpen2]=useState<boolean>(false)
    const [preview,setPreview]=useState(null)
    const navigate=useNavigate()
    const ref=useRef(null)
    const edit=(id:number)=>{
      navigate(`/edit/${id}`)
    }
    const closeModal=()=>{
      ref.current.files=null
      setPreview(null)
      setOpen2(false)

    }
    const deleteHandler=async()=>{
     const res= await fetch(`${BACKEND_URL}/delete_ui/${id}`,{'method':'DELETE'})
     if(res.status==200){
       setData(data=>data.filter(dat=>dat.id!=id))
       setOpen(false)
       setId(null)
     }
    }
    const uploadHandler=async()=>{
      const data=new FormData()
      if(ref.current.files.length>0){

        const file=ref.current.files[0]
        data.append('image',file)
        var res=await fetch(`${BACKEND_URL}/add_data`,{
          method:"POST",
          body:data
        })
        if(res.status==200){
          
          res=await res.json()
          setData(data=>([...data,res.data]))
       
          closeModal()
        }
      }

    }
    useEffect(()=>{
      (async()=>{
        var res=await fetch(`${BACKEND_URL}/get_ui`,{method:"GET"})
        res=await res.json()
        setData(res.data)
      })()
    },[])
const handleImage=(e)=>{
  const file = ref?.current.files[0]; // Access the first selected file
    if (file) {
      const reader = new FileReader();
      
      // Set up the FileReader onload callback to set the image preview
      reader.onloadend = () => {
        setPreview(reader.result); // Set the image preview in state
      };
      
      reader.readAsDataURL(file); // Convert the image to a data URL (Base64)
    }

}
  return (
    <>
    <div className="w-full h-full relative">
    <AlertDialog onOpenChange={setOpen} open={open}>
  <AlertDialogContent>
    <AlertDialogHeader>
      <AlertDialogTitle>Are you absolutely sure?</AlertDialogTitle>
      <AlertDialogDescription>
        This action cannot be undone. This will permanently delete the selected Sketch
        </AlertDialogDescription>
    </AlertDialogHeader>
    <AlertDialogFooter>
      <AlertDialogCancel>Cancel</AlertDialogCancel>
      <AlertDialogAction onClick={deleteHandler}>Continue</AlertDialogAction>
    </AlertDialogFooter>
  </AlertDialogContent>
</AlertDialog>
<Dialog  onOpenChange={closeModal} open={open2}>
  <DialogContent>
    <DialogHeader>
      <DialogTitle>Upload Sketch</DialogTitle>
      <DialogDescription>
      </DialogDescription>
      <div className="w-full px-5 mt-2 h-[300px]">
        {
          preview!=null?
          <img className="w-full h-full object-contain block object-center" src={preview} alt="" />
          :
        <div onClick={()=>ref?.current.click()}  className="w-full cursor-pointer h-full border border-dashed border-black flex flex-col justify-center items-center">
         <UploadIcon className="block"/>
          Upload your sketch Here
        </div>
        }

      </div>
      <input onChange={handleImage}  accept="image/*" className="hidden" type="file" ref={ref}/>
      {
        preview!=null &&
      <div className="flex gap-3 justify-center">
      <Button onClick={()=>ref?.current.click()}  className="w-min  mt-2"><UploadIcon/>Change</Button>
      <Button onClick={uploadHandler} className="w-min  mt-2 bg-green-600 hover:bg-green-400"><UploadIcon/>Upload</Button>

      </div>
      }
    </DialogHeader>
  </DialogContent>
</Dialog>
        <div className="sticky">

        <h1 className="w-full text-center font-bold text-[55px] italic">Sketches</h1>
        <Button onClick={()=>setOpen2(true)} className="absolute top-6 right-16">+ Add Sketch</Button>
        </div>
        <div className="flex w-full flex-wrap justify-center gap-5 overflow-hidden" >
        {
          data.map((sketch,key)=> <div key={key} className="w-[300px] overflow-hidden rounded-xl bg-gray-200 border border-black shadow-xl">
          <img className="block h-[300px] object-cover w-full object-center" src={local_file(`/sketch/${sketch.id}.png`)} alt="" />
          <h1 className="my-2 mx-2 font-bold text-lg">{sketch.name}</h1>
          <div className="flex items-center justify-center mt-1 gap-2 mb-4">
            <Button onClick={()=>edit(sketch.id)}><Edit/>Edit</Button>
            <Button onClick={()=>{setOpen(true);setId(sketch.id)}} variant={'destructive'}><Trash2/>Delete</Button>

          </div>
          </div>)
        }  
        
  
        
        </div>

    </div>
    </>
  )
}

export default Home