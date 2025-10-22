import Logo from '@/assets/logo.jpg'

interface Props {
    title: string
    subtitle?: string
}



export const CustomHeader = ({title, subtitle}: Props) => {
  return (
    <header className="bg-[#134611] text-white py-6 shadow-lg">
      <div className="container mx-auto px-4 flex flex-row items-center">
          <img src={Logo} className="max-w-[100px] rounded-2xl" alt="" />
          <div>
            <h1 className="text-3xl font-bold">{title}</h1>
            <p className="text-[#96E072] ml-15 mt-1">{subtitle}</p>
          </div>
      </div>
    </header>
  )
}
