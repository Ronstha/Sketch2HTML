import { Button } from "@/components/ui/button";
import { BACKEND_URL, local_file } from "@/constant"
import { DeleteIcon, DownloadIcon, FolderIcon, FolderOpenIcon, Fullscreen, ImageIcon, Monitor, MonitorCheck, Trash2 } from "lucide-react"
import { useEffect, useMemo, useRef, useState } from "react"
import { useNavigate, useParams } from "react-router"
import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogFooter,
    DialogHeader,
    DialogTitle,
  } from "@/components/ui/dialog"
const fonts= [
    'Arial',
    'Helvetica',
    'Georgia',
    'Times New Roman',
    'Courier New',
    'Verdana',
    'Roboto', // If you load a Google font or custom font
  ];
const ks=['primary-color','secondary-color','accent-color','primary-text-color','secondary-text-color','background-color','accent-text-color','color','font-family','font-size-lg','font-size-md','font-size-sm','spacing-sm','spacing-md','spacing-lg','border-radius-sm','border-radius-md','border-radius-lg']
const recursive=(node)=>{
    if(node.nodes.length==0) return {[node.id]:{...node,nodes:null}}
    else{
        var prev={}
        node.nodes.forEach(nd=>{
            prev={...prev,...recursive(nd)}
        })
        return {[node.id]:{...node,nodes:null},...prev}
    }


}
function Edit() {
    const {id}=useParams()
    const ref=useRef()
    const [html,setHtml]=useState("")
    const [data,setData]=useState(null)
    const [images,setImages]=useState(null)
    const navigate=useNavigate()
    const byid=useMemo(()=>{
        if(data==null) return []
       return recursive(data)
      
        
    },[data])
    const [name,setName]=useState("")
    const [cur,setCur]=useState(null)
    const [count,setCount]=useState(0)
    const updateStyle=async(name,value)=>{
        await fetch(`${BACKEND_URL}/update_elm/${data.id}`,{method:"POST",
            headers:{
                'Content-Type':'application/json'
            },
            body:JSON.stringify({name:data.name,data:{
                styles:{...data.styles,[name]:value}
            }})
        })
        setCount(count=>count+1)
           
    }
    useEffect(()=>{
        (async()=>{
           var res= await fetch(`${BACKEND_URL}/get_imagelist`)
           res=await res.json()
           setImages(res)
        })()

    },[])
    useEffect(()=>{
        (async()=>{
            var res=await fetch(`${BACKEND_URL}/get_ui/${id}`,{method:"get"})
            if(res.status==200){
                res=await res.json()
                setHtml(res.html.replace(/<a/g,"<div").replace(/<\/a/g,"</div"))
                setData(res.node)
                setName(res.name)
              
            }
            
        })()
    },[id,count])
    const doSomething=(e)=>{
        e.target.contentWindow.addEventListener('click',e=>{
            e.preventDefualt()

        })
        e.target.contentWindow.addEventListener('dblclick',e=>{
           setCur(byid[parseInt(e.target.dataset.id)])
        })
        
    }
    const saveHandler=()=>{
        window.open(`${BACKEND_URL}/save_file/${id}`)
    }
    const fullPreview=()=>{
       const win= window.open()
       win?.document.write(html)
    }
  return (
    <div>

    <div></div>
   <div className=" h-full w-full relative overflow-y-auto">
    <div className="font-bold text-xl hover:text-slate-400 cursor-pointer" onClick={()=>navigate('/')}>{"< Back"}</div>
        <div className="w-screen h-screen top-1 left-2 scale-[.7] mt-8 absolute origin-top-left">
            <iframe onLoad={doSomething}  className="border border-black w-full h-full rounded-md" srcDoc={html} id="frame"   frameBorder="1"></iframe>
        <div className="flex gap-3 scale-[1.45] origin-top-left mt-10">
            <Button onClick={fullPreview}><Monitor/>Full Preview</Button>
            <Button onClick={saveHandler}><DownloadIcon/>Save</Button>
        </div>
        </div>
        <div className="ml-auto w-[22%] h-[300px] bg-slate-200 px-2 py-4 overflow-y-auto">
        <div className="sticky text-center font-bold">Styling</div>
   
        {
            data!=null &&
            <>
            <StyleForm styles={data.styles} updateStyle={updateStyle}/>
            </>

        }
        </div>
        <div className="ml-auto w-[22%] h-[400px] bg-slate-200 px-2 py-4 overflow-y-auto mt-5">
        {
            cur!=null &&
            <>
            <EditElement images={images} setImages={setImages} elm={cur} setCount={setCount}/>            
            </>
        }
        </div>
        
   </div>
    </div>
  )
}
function EditElement({elm,setCount,images,setImages}){
    const ref=useRef()
    const [value,setValue]=useState(null)
    const [open,setOpen]=useState(false)
    const [type,setType]=useState('url')
    const [preview,setPreview]=useState(null)
    const [url,setUrl]=useState('')
    const parseImage=(url)=>{
       
        if(url.slice(0,4)=='http'){
            return url
        }else{
            return local_file('/'+url)
        }
    }
    const deleteImageHandler=async(id)=>{
        if(window.confirm('Are you sure? You want to remove this image?')){
          const res=  await fetch(`${BACKEND_URL}/remove_image/${id}`,{method:"DELETE"})
          if(res.status==200){
            setImages(images.filter(img=>img.id!=id))
          }
        }
    }
    const addImageHandler=async()=>{
        let headers,data;
        if(type=='local'){
             headers={} 
             data=new FormData()
             data.append('image',ref.current.files[0])
        }else{
            
            if (url==""||url.slice(0,4)!='http') return
             headers={'Content-Type':'application/json'}
             data=JSON.stringify({url})
        }
       var res=await fetch(`${BACKEND_URL}/add_image/${type=='local'?0:1}`,{
            method:'POST',
            headers,body:data
        })
        if(res.status==200){
            res=await res.json()
            setImages(images=>([...images,res]))
            setUrl('');
            if(ref?.current) ref.current.files=null;
            setPreview(null)
        }


    }
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
    useEffect(()=>{
        if(['text','navlink','paragraph','button','button-c','button-r','text-c','text-r'].includes(elm.element)){
            setValue(elm.text)
        }
        else if(elm.element=='image'){
            setValue([elm.url])
        }else if(elm.element=='carousel'){
            setValue(elm.images.filter(im=>!images.includes(im.url)))
        }
    },[elm])
    
    const saveHandler=async()=>{
        const dict={
            'image':'url',
            'carousel':'images'
        }   
        await fetch(`${BACKEND_URL}/update_elm/${elm.id}`,{method:"POST",
            headers:{
                'Content-Type':'application/json'
            },
            body:JSON.stringify({name:elm.name,data:{
                [dict[elm.element]??'text']:elm.element=='image'?value[0]:value
            }})
        })
        setCount(count=>count+1)
        
    }
    const selectHandler=(im)=>{
        if(elm.element=='image'){
            setValue([im.url])
        }else{
            setValue(value=>{
                if(value.includes(im.url)){
             
                    return value.filter(img=>img!=im.url)
                }
                return [...value,im.url]
            })
        }
    }
    if(value==null) return <></>
    if(['text','navlink','paragraph','button','button-c','button-r','text-c','text-r'].includes(elm.element)){
        return <>
        <div className="text-center font-bold">Edit Value</div>
        {
            elm.element=='paragraph'?
            <textarea autoFocus rows={5} className="px-2 py-2 mt-2 font-md w-full rounded-md outline-none border border-black resize-none" onChange={e=>setValue(e.target.value)} value={value}></textarea>
            :
        <input autoFocus className="px-2 py-2 mt-2 font-md rounded-md outline-none border border-black " onChange={e=>setValue(e.target.value)} value={value} type="text" />
        }
        <Button onClick={saveHandler}>Save</Button>
        </>
        }
    else if(['image','carousel'].includes(elm.element)){
   
        return <>
         <Dialog   onOpenChange={setOpen} open={open}>
      
      <DialogContent className="w-[1000px] overflow-auto max-h-[80%]">
        <DialogHeader>
          <DialogTitle>Image Picker</DialogTitle>
          <DialogDescription>
            Select Images From Here
          </DialogDescription>
        </DialogHeader>
       
        <div className="w-full mt-5 px-2 flex flex-wrap gap-3 space-y-2">
        
        {
            images.map((image,key)=><div onClick={()=>selectHandler(image)} className={`${value.includes(image.url)?'border-red-600 border-[3px] ':'border-black '}cursor-pointer w-[100px] relative aspect-square border`} key={key}>
                <img className="w-full h-full block object-cover object-center" src={parseImage(image.url)} alt="image" />
                <div className="text-red-500 absolute right-1 top-1">
                    <Trash2 onClick={()=>deleteImageHandler(image.id)} size={20} className="cursor-pointer"/>
                </div>
            </div>)    
        }
        </div>
       
        <DialogFooter>
            <div className="w-full">

            <div className="flex flex-col gap-3 my-3">
        <select value={type}  onChange={e=>setType(e.target.value)} className="outline-none border border-black px-2 py-2 rounded-md"> 
            <option value={'local'}>Image</option>
            <option value={'url'}>Url</option>
        </select>
        {
            type=='url' ?
            <input value={url} onChange={e=>setUrl(e.target.value)} className="px-2 py-2 border border-black rounded-md outline-none" placeholder="Enter Url" type="text"/>
            :
            <>
     
            <div className="w-full aspect-square px-3 mt-3 py-2">
                {
                    preview==null?
                <div onClick={()=>ref.current.click()} className="w-full aspect-square border border-black border-dashed flex flex-col items-center justify-center cursor-pointer">
                    <div>Select Image to Upload</div>
                </div>:
                <img onDoubleClick={()=>ref.current.click()} className="w-full h-full object-contain block object-center cursor-pointer" src={preview} alt="image" />
                }
                <input onChange={handleImage}  accept="image/*" className="hidden" type="file" ref={ref} />


            </div>
            </>
        }
        </div>
        <Button onClick={addImageHandler}><ImageIcon/> Add Image</Button>
            </div>
        </DialogFooter>
      </DialogContent>
    </Dialog>
        <div className="text-center font-bold py-2">Select Image{elm.element=='carousel' && 's'}</div>
        <div className="flex flex-wrap gap-2 w-full h-[250px] overflow-y-auto">
            {value.length>0 &&
               ( elm.element=='image'?
                <img src={parseImage(value[0])} alt="image" className="h-full w-full block object-contain object-center"/>
                :
                value.map((img,key)=><img className="block aspect-square object-contain w-[100px] object-center" src={parseImage(img)} key={key} alt={'image'+key.toString()}/>)
               )
            }
            
        </div>
        <div className="mt-2 flex gap-3 justify-center">

        <Button className="" onClick={()=>setOpen(true)}>{value.length==0?'Select':'Change'}</Button>
        <Button className="" onClick={saveHandler}>Save</Button>
        </div>
        </>
    }
}
function StyleForm({styles,updateStyle}){
    const styling=useMemo(()=>{
        const stl=[]
      ks.forEach(k=>{
            var type;
            if(k.includes('color')){
                type='color'
            }else if(k=='font-family'){
                type='font'
            }else{
                type="number"
            }
                stl.push({
                    name:k,
                    type:type,
                    label:k,
                    value:styles[k]
                })
           
        })
        return stl
    },[styles])

    return <>
    <div className="">
    {
                styling.map((stl,key)=><div key={key} className="flex items-center">
            
                <label htmlFor={stl.name} className="font-bold text-md">{stl.label}</label>
                {
                    stl.type=='color' &&
                    <input onChange={e=>updateStyle(stl.name,e.target.value)} defaultValue={stl.value} name={stl.name} type="color" className="h-8 w-8 mx-2 outline-none p-0 border cursor-pointer" />
                }
                {
                    stl.type=='font' &&
<select onChange={e=>updateStyle(stl.name,e.target.value)} className="outline-none mx-2 my-2 py-2 rounded-sm border border-black" name={stl.name} defaultValue={stl.value}>
    {
        fonts.map((font,key)=><option key={key} value={font}>{font}</option>)
    }

</select>
}
{
    stl.type=='number' &&<>
    <NumberInput updateStyle={updateStyle} value={stl.value} name={stl.name}/>
  
    </>
}
    
            </div>)
            }
        
        

    </div>
    </>
}

function Tree({node,cur,setCur}){
    const [hide,setHide]=useState(true)
    const selectHandler=()=>{
        
        const nd={...node}
        delete nd.nodes
        setCur(nd)
    
        setHide(hide=>!hide)
    }
    return <>
    <div className="hidden">
        <div className={`${cur?.id==node.id?'text-white bg-blue-500 ':''}cursor-pointer select-none h-5 flex items-center ml-4 hover:bg-blue-500 font-bold hover:text-white p-2`} onClick={selectHandler}>{node.nodes.length!=0 && (!hide?<FolderOpenIcon className="mr-2" size={20}/>:<FolderIcon className="mr-2" size={20}/>)}{node.element}</div>

        <div className="mx-4">
            
            {
                !hide &&
                node.nodes.map((child,key)=><Tree cur={cur} setCur={setCur} node={child} key={key}/>)
            }

        </div>
    </div>
    </>
}
const NumberInput=({value:initval,name,updateStyle})=>{
    const [val,setVal]=useState(parseFloat(initval))
    const [unit,setUnit]=useState(initval.replace(/\d/g, ''))
    const [value,setValue]=useState(initval)
    const [first,setFirst]=useState(true)
    useEffect(()=>{
 if(first){
    setFirst(false)
    return
 }
    updateStyle(name,value)
        
    },[value])
    return <>
{
    value!=null &&
    <>
    <input  onChange={(e)=>{setVal(parseFloat(e.target.value));setValue(`${e.target.value}${unit}`)}} value={val} type="number" className="w-[80px] mx-2 my-2 border border-black rounded-md px-2" />
      <select onChange={(e)=>{setUnit(e.target.value);setValue(`${val}${e.target.value}`)}} value={unit}>
            <option value={'px'}>px</option>
            <option value={'rem'}>rem</option>
            <option value={'em'}>em</option>
      </select>
    </>
}

        

      
    </>

}
export default Edit