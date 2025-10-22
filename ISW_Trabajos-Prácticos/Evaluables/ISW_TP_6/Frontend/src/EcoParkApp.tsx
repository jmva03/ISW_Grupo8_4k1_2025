import { CustomHeader } from "./components/custom/CustomHeader"
import { ActivityRegistrationForm } from "./pages/Reservation"



export const EcoParkApp = () => {
  return (
    <div className="min-h-screen bg-linear-to-br from-[#E8FCCF] to-[#96E072]/30">
      <CustomHeader title="🌲 Parque de Aventuras" subtitle="Sistema de Inscripciones"></CustomHeader>
      <div className="py-12 px-4 lg:px-8">
        <div className="container mx-auto">
          <ActivityRegistrationForm/>
        </div>
      </div>
    </div>
  )
}
