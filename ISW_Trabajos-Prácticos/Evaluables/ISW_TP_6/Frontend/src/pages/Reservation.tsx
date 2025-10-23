import { useState, useEffect, useMemo } from "react"
import { Toaster, toast } from "sonner"
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Checkbox } from "@/components/ui/checkbox"
import { Button } from "@/components/ui/button"
import { Separator } from "@/components/ui/separator"
import { Calendar } from "@/components/ui/calendar"
import { AnimatePresence, motion, type Variants } from "framer-motion"
import { Skeleton } from "@/components/ui/skeleton"
import { cn } from "@/lib/utils"
import {
 Accordion,
 AccordionContent,
 AccordionItem,
 AccordionTrigger,
} from "@/components/ui/accordion"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
  DialogFooter,
  DialogClose,
} from "@/components/ui/dialog"
export interface DataResponse {
  actividad_id: number
  actividad: string
  requiere_talla: number // This is a boolean (0 or 1)
  edad_minima: null
  turnos: Turno[]
}

export interface Turno {
  id: number
  inicio: string
  fin: string
  cupos_disponibles: number
}

interface ParticipantDetails {
  fullName: string
  dni: string
  age: string
  clothingSize?: string
}

const activityConfig = {
  Tirolesa: { id: 1, requiere_talla: 1 },
  Safari: { id: 2, requiere_talla: 0 },
  Palestra: { id: 3, requiere_talla: 1 },
  Jardinería: { id: 4, requiere_talla: 0 },
} as const

type ActivityName = keyof typeof activityConfig

const clothingSizes = ["XS", "S", "M", "L", "XL"]

export function ActivityRegistrationForm() {
  const [selectedDate, setSelectedDate] = useState<Date | undefined>(undefined)
  const [selectedActivity, setSelectedActivity] = useState<ActivityName | "">("")
  const [selectedTimeSlot, setSelectedTimeSlot] = useState<string>("")
  const [availableTimeSlots, setAvailableTimeSlots] = useState<Turno[]>([])
  const [isLoadingTimeSlots, setIsLoadingTimeSlots] = useState(false)
  const [timeSlotError, setTimeSlotError] = useState<string>("")
  const [numberOfParticipants, setNumberOfParticipants] = useState<string>("1")
  const [participants, setParticipants] = useState<ParticipantDetails[]>([
    { fullName: "", dni: "", age: "", clothingSize: "" },
  ])
  const [termsAccepted, setTermsAccepted] = useState(false)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [submitError, setSubmitError] = useState<string | null>(null)
  const [minAgeForActivity, setMinAgeForActivity] = useState<number | null>(null)
  const [clientErrors, setClientErrors] = useState<Record<number, { dni?: string; name?: string; age?: string }>>({});

  const [currentFormStep, setCurrentFormStep] = useState("step-1")
  const requiresClothingSize = selectedActivity ? activityConfig[selectedActivity].requiere_talla === 1 : false

  const selectedSlotDetails = useMemo(() => {
      if (!selectedTimeSlot) return null
      // Busca el turno completo usando el ID guardado en selectedTimeSlot
      return availableTimeSlots.find(
        (turno) => turno.id.toString() === selectedTimeSlot,
      )
    }, [selectedTimeSlot, availableTimeSlots])


  const maxParticipants = selectedSlotDetails?.cupos_disponibles
  
  const resetForm = () => {
      setSelectedDate(undefined)
      setSelectedActivity("")
      setSelectedTimeSlot("")
      setAvailableTimeSlots([])
      setTimeSlotError("")
      setNumberOfParticipants("1")
      setParticipants([{ fullName: "", dni: "", age: "", clothingSize: "" }])
      setTermsAccepted(false)
      setSubmitError(null)
      setCurrentFormStep("step-1")
      setMinAgeForActivity(null) // <-- AÑADIR
      setClientErrors({}) // <-- AÑADIR
    }

// --- FUNCIONES DE VALIDACIÓN (PASO 3A, 3B, 3C) ---
  
  const validateName = (name: string): string | null => {
    if (/\d/.test(name)) { // Regex para buscar cualquier dígito
      return "El nombre no puede contener números."
    }
    return null
  }

  const validateDNI = (dni: string): string | null => {
    if (!/^\d+$/.test(dni)) { // Regex para solo números
      return "El DNI debe contener solo números."
    }
    if (dni.length < 7 || dni.length > 8) {
      return "El DNI debe tener entre 7 y 8 dígitos."
    }
    return null
  }

  const validateAge = (age: string, minAge: number | null): string | null => {
    const ageNum = Number.parseInt(age, 10)
    if (isNaN(ageNum) || ageNum <= 0) {
      return "Edad inválida."
    }
    if (minAge && ageNum < minAge) {
      return `La edad mínima para esta actividad es ${minAge} años.`
    }
    return null
  }


  const isDateDisabled = (date: Date) => {
    const today = new Date()
    today.setHours(0, 0, 0, 0)
    const twoDaysFromNow = new Date(today)
    twoDaysFromNow.setDate(today.getDate() + 2)

    if (date < twoDaysFromNow) {
      return true
    }

    const dayOfWeek = date.getDay()
    if (dayOfWeek === 0 || dayOfWeek === 6) {
      return true
    }

    const month = date.getMonth()
    const day = date.getDate()
    if ((month === 0 && day === 1) || (month === 11 && day === 25)) {
      return true
    }

    return false
  }

useEffect(() => {
    const fetchTimeSlots = async () => {
      if (!selectedDate || !selectedActivity) {
        setAvailableTimeSlots([])
        return
      }

      setIsLoadingTimeSlots(true)
      setTimeSlotError("") // Limpiamos errores anteriores
      setSelectedTimeSlot("") // Reseteamos el turno

    try {
      const year = selectedDate.getFullYear()
      const month = String(selectedDate.getMonth() + 1).padStart(2, "0")
      const day = String(selectedDate.getDate()).padStart(2, "0")
      const formattedDate = `${year}-${month}-${day}`

      const activityId = activityConfig[selectedActivity].id
      const url = `http://127.0.0.1:8000/disponibilidad?dia=${formattedDate}&actividad_id=${activityId}`

      console.log("[v0] Fetching time slots from:", url)

      const response = await fetch(url)
      if (!response.ok) {
        throw new Error("Error al conectar con el servidor.")
      }
      
      const dataResponse = await response.json()

      // --- AQUÍ ESTÁ LA SOLUCIÓN ---
      // Si el array está vacío, significa que el parque está cerrado para esa selección.
      if (!dataResponse || dataResponse.length === 0) {
        console.log("[v0] Received empty array, park is closed for this selection.")
        
        // Disparamos el toast que querías
        toast.info("El parque está cerrado ese día para esta actividad.", {
          description: "Por favor, selecciona otra fecha o actividad.",
          position: "top-center",
        })
        
        setAvailableTimeSlots([]) // Dejamos los turnos vacíos
        setIsLoadingTimeSlots(false) // Paramos la carga
        return // Salimos de la función 'try'
      }
      // --- FIN DE LA SOLUCIÓN ---

      // Si llegamos aquí, dataResponse[0] SÍ existe
      const data: DataResponse = dataResponse[0] 
      console.log("[v0] Received time slots:", data)
      setMinAgeForActivity(data.edad_minima || null)
      const availableSlots = data.turnos ? data.turnos.filter((turno) => turno.cupos_disponibles > 0) : []

      if (availableSlots.length === 0) {
        // Esta lógica ahora solo se activa si la actividad existe, pero todos los turnos están llenos.
        toast.info("No hay cupos disponibles.", {
          description: "Todos los turnos para esta actividad ya están llenos.",
          position: "top-center",
        })
        setAvailableTimeSlots([])
      } else {
        // Caso exitoso: hay slots
        setAvailableTimeSlots(availableSlots)
      }

    } catch (error) {
        console.error("[v0] Error fetching time slots:", error)
        const errorMessage = error instanceof Error ? error.message : "No se pudieron cargar los turnos."
        
        // Los errores de red SÍ los mostramos en el toast Y en el acordeón
        setTimeSlotError(errorMessage) 
        setAvailableTimeSlots([])
        toast.error(errorMessage, { position: "top-center" })

      } finally {
        setIsLoadingTimeSlots(false)
      }
    }

    fetchTimeSlots()
  }, [selectedDate, selectedActivity])

  useEffect(() => {
    let count = Number.parseInt(numberOfParticipants, 10);
 
    // 2. Validamos que sea un número válido y mayor a 0
    if (isNaN(count) || count < 1) {
      count = 1;
    }
 
    // 3. (Opcional pero recomendado) Validamos contra el máximo
    if (maxParticipants && count > maxParticipants) {
      count = maxParticipants;
    }
    setParticipants((prev) => {
      const newParticipants = Array.from({ length: count }, (_, i) => {
        return prev[i] || { fullName: "", dni: "", age: "", clothingSize: "" }
      })
      return newParticipants
    })
  }, [numberOfParticipants, maxParticipants])

  useEffect(() => {
      const currentCount = Number.parseInt(numberOfParticipants)
      // Si hay un máximo de participantes y el número actual es mayor...
      if (maxParticipants && currentCount > maxParticipants) {
        // ...reduce el número de participantes al máximo permitido
        setNumberOfParticipants(maxParticipants.toString())
      }
    }, [maxParticipants, numberOfParticipants])


const updateParticipant = (index: number, field: keyof ParticipantDetails, value: string) => {
    // 1. Actualiza el estado del participante (esto está bien)
    setParticipants((prev) => {
      const updated = [...prev]
      updated[index] = { ...updated[index], [field]: value }
      return updated
    })

    // 2. Ejecuta la validación y actualiza el estado de errores (AQUÍ LA CORRECCIÓN)
    setClientErrors((prevErrors) => {
      // Copia los errores específicos de ESTE participante
      const newErrors = { ...prevErrors[index] }
      let error: string | null = null
      let fieldName: "name" | "dni" | "age" | undefined; // Necesitamos saber qué campo es

      if (field === "fullName") {
        fieldName = "name"
        error = validateName(value)
      } else if (field === "dni") {
        fieldName = "dni"
        error = validateDNI(value)
      } else if (field === "age") {
        fieldName = "age"
        error = validateAge(value, minAgeForActivity)
      }

      // Si es un campo que validamos...
      if (fieldName) {
        if (error) {
          // Si hay un error, lo establecemos
          newErrors[fieldName] = error
        } else {
          // Si NO hay error, ELIMINAMOS la clave
          delete newErrors[fieldName]
        }
      }

      // Devolvemos el estado de errores actualizado
      return {
        ...prevErrors,
        [index]: newErrors,
      }
    })
  }
const isFormValid = () => {
    if (!selectedDate || !selectedActivity || !selectedTimeSlot || !termsAccepted) {
      return false
    }

    const count = Number.parseInt(numberOfParticipants, 10)
    if (isNaN(count) || count < 1) {
      return false // Deshabilita el botón si es 0, NaN, o < 1
    }

    const hasClientErrors = Object.values(clientErrors).some(
      (participantErrors) => Object.keys(participantErrors).length > 0,
    )
    if (hasClientErrors) {
      return false
    }

    // 3. Comprueba que todos los campos estén llenos (como antes)
    return participants.every((participant) => {
      const basicFieldsFilled =
        participant.fullName.trim() !== "" && participant.dni.trim() !== "" && participant.age.trim() !== ""

      if (requiresClothingSize) {
        return basicFieldsFilled && !!participant.clothingSize
      }
      return basicFieldsFilled
    })
  }

const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!isFormValid()) {
      console.warn("Form is invalid, submission blocked.")
      return
    }

    setIsSubmitting(true)
    setSubmitError(null)

    // 1. Construir el payload con los nombres correctos
    const payload = {
      id_turno: Number.parseInt(selectedTimeSlot),
      cantidad: Number.parseInt(numberOfParticipants),
      tyc: termsAccepted ? 1 : 0,
      participantes: participants.map((p) => ({
        nombre: p.fullName,
        edad: Number.parseInt(p.age, 10), // Asegúrate de que la edad sea un número
        dni: p.dni,
        // Envía el talle solo si es requerido y tiene valor, sino envía null
        talla_vestimenta: requiresClothingSize ? p.clothingSize || null : null,
      })),
    }

    console.log("[v0] Submitting reservation with payload:", JSON.stringify(payload, null, 2))

    try {
      // 2. Enviar la petición POST
      // Asumo el endpoint basado en tu URL anterior
      const response = await fetch("http://127.0.0.1:8000/inscripciones", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      })

      if (!response.ok) {
        // Intenta leer un mensaje de error del backend
        const errorData = await response.json().catch(() => ({})); // Intenta parsear el JSON
        let errorMessage = "No se pudo realizar la inscripción. Intenta de nuevo."
      
        // Comprueba si viene el formato {"detail": {"status": "...", "message": "..."}}
        if (errorData.detail && errorData.detail.message) {
          errorMessage = errorData.detail.message;
        }
        // Comprueba si viene un error simple {"detail": "..."}
        else if (errorData.detail) {
          errorMessage = errorData.detail;
        }        
        
        
        
        throw new Error(errorMessage)
      }

      // 3. Éxito
      const result = await response.json()
      console.log("Reservation successful:", result)
      toast.success("Reservation submitted successfully!")
      resetForm()

    } catch (error) {
      // 4. Manejo de errores
      console.error("[v0] Error submitting reservation:", error)
      const errorMessage = error instanceof Error ? error.message : "An unknown error occurred during submission."
      setSubmitError(errorMessage)
      toast.error("Error en la Inscripción", {
        description: errorMessage,
        position: "top-center",
      })
    } finally {
      setIsSubmitting(false)
    }
  }


  const sectionVariants: Variants = {
      hidden: { opacity: 0, y: -10 },
      visible: { opacity: 1, y: 0, transition: { duration: 0.3, ease: "easeInOut" } },
      exit: { opacity: 0, y: -10, transition: { duration: 0.2 } },
    }

    const TimeSlotSkeletons = () => (
      <div className="space-y-3">
        <Skeleton className="h-5 w-3/4" />
        <Skeleton className="h-5 w-1/2" />
        <Skeleton className="h-5 w-2/3" />
      </div>
    )
// ... (después de tus funciones de validación)

  const handleParticipantsBlur = () => {
    let count = Number.parseInt(numberOfParticipants, 10);

    // Si no es un número o es menor a 1...
    if (isNaN(count) || count < 1) {
      // ...lo reseteamos a "1".
      setNumberOfParticipants("1");
    }
    // Si excede el máximo...
    else if (maxParticipants && count > maxParticipants) {
      // ...lo reseteamos al máximo.
      setNumberOfParticipants(maxParticipants.toString());
    }
  };


  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle className="text-2xl">Book Your Activity</CardTitle>
      </CardHeader>
      <Toaster richColors position="top-center" />
      <form onSubmit={handleSubmit}>
        <CardContent className="grid grid-cols-1 md:grid-cols-2 md:gap-8 space-y-6 md:space-y-0">
        {/* --- COLUMNA 1: CALENDARIO --- */}
          <div className="space-y-2">
            <Label>Select a Date</Label>
            <Calendar
              mode="single"
              selected={selectedDate}
              // --- ESTE BLOQUE ES EL QUE CAMBIA ---
              onSelect={(date) => {
                // 1. Establece la nueva fecha
                setSelectedDate(date)

                // 2. Resetea TODOS los estados siguientes
                setSelectedActivity("")
                setSelectedTimeSlot("")
                setAvailableTimeSlots([]) // Limpia los turnos viejos
                setTimeSlotError("")
                setNumberOfParticipants("1")
                setParticipants([{ fullName: "", dni: "", age: "", clothingSize: "" }])
                setTermsAccepted(false)
                setMinAgeForActivity(null) // <-- AÑADIR
                setClientErrors({}) // <-- AÑADIR

                // 3. Mueve el acordeón al Paso 1 (Actividad)
                // (O al paso 2 si quieres que salte directo a turnos, 
                // pero "step-1" es un reseteo más limpio)
                setCurrentFormStep("step-1")
              }}
                disabled={isDateDisabled}
                className="rounded-md border"
              />
            </div>
          
          <div className="space-y-6">
           <Accordion
             type="single"
             collapsible
             className="w-full"
             value={currentFormStep}
             onValueChange={setCurrentFormStep}
           >
             {/* --- PASO 1: ACTIVIDAD --- */}
             <AccordionItem value="step-1">
               <AccordionTrigger className="text-lg font-semibold">
                 Paso 1: Elige una Actividad
               </AccordionTrigger>
               <AccordionContent>
                 {/* Mensaje para guiar al usuario */}
                 {!selectedDate && (
                   <p className="mb-4 text-sm text-muted-foreground">
                     Por favor, selecciona primero una fecha en el calendario.
                   </p>
                 )}
                 <div className="space-y-2">
                   <Label htmlFor="activity">Actividad</Label>
                   <Select
                     value={selectedActivity}
                     onValueChange={(value) => {
                       setSelectedActivity(value as ActivityName)
                       setCurrentFormStep("step-2") // <-- Avanza al siguiente paso
                     }}
                     disabled={!selectedDate} // Deshabilitado si no hay fecha
                   >
                     <SelectTrigger id="activity">
                       <SelectValue placeholder="Selecciona una actividad" />
                     </SelectTrigger>
                     <SelectContent>
                       {(Object.keys(activityConfig) as ActivityName[]).map((activityName) => (
                         <SelectItem key={activityName} value={activityName}>
                           {activityName}
                         </SelectItem>
                       ))}
                     </SelectContent>
                   </Select>
                 </div>
               </AccordionContent>
             </AccordionItem>
             {/* --- PASO 2: TURNO --- */}
              {/* --- PASO 2: TURNO --- */}
            <AccordionItem value="step-2" disabled={!selectedActivity}>
              <AccordionTrigger className="text-lg font-semibold">
                Paso 2: Elige un Turno
              </AccordionTrigger>
              <AccordionContent>
                <div className="space-y-3">
                  
                  {/* 1. Muestra Skeletons si está cargando */}
                  {isLoadingTimeSlots && (
                    <TimeSlotSkeletons />
                  )}

                  {/* 2. Muestra el error de red si existe */}
                  {!isLoadingTimeSlots && timeSlotError && (
                    <p className="text-sm text-destructive">{timeSlotError}</p>
                  )}

                  {/* 3. Muestra los turnos si hay y no hay error */}
                  {!isLoadingTimeSlots && !timeSlotError && availableTimeSlots.length > 0 && (
                    <RadioGroup
                      value={selectedTimeSlot}
                      onValueChange={(value) => {
                        setSelectedTimeSlot(value)
                        setCurrentFormStep("step-3") // Avanza al siguiente paso
                      }}
                      className="w-full"
                    >
                      {/* Tu grid de tarjetas de turnos */}
                      <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
                        {availableTimeSlots.map((turno) => (
                          <div key={turno.id}>
                            <RadioGroupItem
                              value={turno.id.toString()}
                              id={`turno-${turno.id}`}
                              className="sr-only"
                            />
                            <Label
                              htmlFor={`turno-${turno.id}`}
                              className={cn(
                                "flex flex-col items-center justify-between rounded-md border-2 border-muted bg-transparent p-4 hover:bg-accent hover:text-accent-foreground cursor-pointer transition-colors duration-150",
                                selectedTimeSlot === turno.id.toString() && "border-primary bg-accent"
                              )}
                            >
                              <span className="font-bold text-lg">{turno.inicio}</span>
                              <span className="text-xs text-center text-muted-foreground uppercase">
                                Quedan {turno.cupos_disponibles} cupos
                              </span>

                            </Label>
                          </div>
                        ))}
                      </div>
                    </RadioGroup>
                  )}
                  
                  {/* 4. No se muestra nada (null) si no hay carga, no hay error y no hay slots */}

                </div>
              </AccordionContent>
            </AccordionItem>
            {/* --- PASO 3: DETALLES --- */}
            <AccordionItem value="step-3" disabled={!selectedTimeSlot}>
              <AccordionTrigger className="text-lg font-semibold">
                Paso 3: Completa tus Datos
              </AccordionTrigger>
              <AccordionContent className="space-y-6">
                
                {/* 1. NÚMERO DE PARTICIPANTES (SIEMPRE VISIBLE EN ESTE PASO) */}
                <div className="space-y-2">
                  <Label htmlFor="participants">Número de Participantes</Label>
                  <Input
                    id="participants"
                    type="number"
                    min="1"
                    max={maxParticipants}
                    value={numberOfParticipants}
                    onChange={(e) => setNumberOfParticipants(e.target.value)}
                    disabled={!maxParticipants}
                    onBlur={handleParticipantsBlur}
                  />
                </div>

                {/* 2. CONTENEDOR CONDICIONAL (SOLO APARECE SI HAY PARTICIPANTES) */}
                {Number.parseInt(numberOfParticipants) > 0 && (
                  <> {/* Usamos un Fragmento para no añadir un div que rompa el space-y-6 */}
                    
                    {/* 2A. DETALLES DE PARTICIPANTES (EL .MAP) */}
                    <div className="space-y-4">
                      <h3 className="text-lg font-semibold">Detalles de Participantes</h3>
                      {participants.map((participant, index) => (
                        <div key={index}>
                          {index > 0 && <Separator className="my-4" />}
                          <div className="space-y-4">
                            <h4 className="font-medium text-muted-foreground">Participante {index + 1}</h4>

                            {/* Nombre Completo */}
                              <div className="space-y-2">
                              <Label htmlFor={`fullName-${index}`}>Nombre Completo</Label>
                              <Input
                                id={`fullName-${index}`}
                                value={participant.fullName}
                                onChange={(e) => updateParticipant(index, "fullName", e.target.value)}
                                placeholder="Ingresa el nombre"
                              />
                              {/* --- MOSTRAR ERROR DE CLIENTE --- */}
                              {clientErrors[index]?.name && (
                                <p className="text-sm text-destructive">{clientErrors[index].name}</p>
                              )}
                            </div>

                            {/* DNI */}
                            <div className="space-y-2">
                              <Label htmlFor={`dni-${index}`}>DNI</Label>
                              <Input
                                id={`dni-${index}`}
                                value={participant.dni}
                                onChange={(e) => updateParticipant(index, "dni", e.target.value)}
                                placeholder="Ingresa el DNI"
                              />
                              {/* --- MOSTRAR ERROR DE CLIENTE --- */}
                              {clientErrors[index]?.dni && (
                                <p className="text-sm text-destructive">{clientErrors[index].dni}</p>
                              )}
                            </div>

                            {/* Edad */}
                            <div className="space-y-2">
                              <Label htmlFor={`age-${index}`}>Edad</Label>
                              <Input
                                id={`age-${index}`}
                                type="number"
                                min="1"
                                max="120"
                                value={participant.age}
                                onChange={(e) => updateParticipant(index, "age", e.target.value)}
                                placeholder="Ingresa la edad"
                              />
                              {/* --- MOSTRAR ERROR DE CLIENTE --- */}
                              {clientErrors[index]?.age && (
                                <p className="text-sm text-destructive">{clientErrors[index].age}</p>
                              )}
                            </div>

                            {/* Talle (Condicional) */}
                            {requiresClothingSize && (
                              <div className="space-y-2">
                                <Label htmlFor={`clothingSize-${index}`}>Talle de Vestimenta</Label>
                                <Select
                                  value={participant.clothingSize}
                                  onValueChange={(value) => updateParticipant(index, "clothingSize", value)}
                                >
                                  <SelectTrigger id={`clothingSize-${index}`}>
                                    <SelectValue placeholder="Selecciona un talle" />
                                  </SelectTrigger>
                                  <SelectContent>
                                    {clothingSizes.map((size) => (
                                      <SelectItem key={size} value={size}>
                                        {size}
                                      </SelectItem>
                                    ))}
                                  </SelectContent>
                                </Select>
                              </div>
                            )}
                          </div>
                        </div>
                      ))}
                    </div>

                    {/* 2B. TÉRMINOS Y CONDICIONES */}
{/* 2B. TÉRMINOS Y CONDICIONES (CON MODAL) */}
                    <Dialog>
                      <div className="flex items-start space-x-2">
                        <Checkbox
                          id="terms"
                          checked={termsAccepted}
                          onCheckedChange={(checked) => setTermsAccepted(checked === true)}
                        />
                        <div className="grid gap-1.5 leading-relaxed">
                          <Label htmlFor="terms" className="text-sm">
                            Acepto los{" "}
                            <DialogTrigger asChild>
                              <span className="text-primary font-semibold underline cursor-pointer hover:text-eco-dark">
                                términos y condiciones
                              </span>
                            </DialogTrigger>
                            {" "}de la actividad {" "}
                            <span className="font-semibold">{selectedActivity}</span>.
                          </Label>
                        </div>
                      </div>

                      {/* CONTENIDO DEL MODAL */}
                      <DialogContent className="sm:max-w-md">
                        <DialogHeader>
                          <DialogTitle>Términos y Condiciones - EcoHarmony Park</DialogTitle>
                          <DialogDescription>
                            Al inscribirse, el visitante declara haber leído y aceptado los siguientes términos:
                          </DialogDescription>
                        </DialogHeader>
                        <div className="space-y-4 text-sm text-muted-foreground max-h-[400px] overflow-y-auto pr-4">
                          <p>
                            <strong>Responsabilidad personal:</strong> El participante asume la responsabilidad por su estado físico y condiciones de salud necesarias para realizar la actividad elegida.
                          </p>
                          <p>
                            <strong>Cumplimiento de normas:</strong> Durante la actividad deberá seguir en todo momento las indicaciones del personal del parque y respetar las normas de seguridad.
                          </p>
                          <p>
                            <strong>Uso de equipamiento:</strong> En las actividades que lo requieran (Tirolesa, Palestra), es obligatorio el uso del equipamiento y vestimenta provistos por el parque.
                          </p>
                          <p>
                            <strong>Edad mínima:</strong> Cada actividad tiene una edad mínima establecida. El registro de una edad incorrecta podrá invalidar la inscripción.
                          </p>
                          <p>
                            <strong>Cupos y horarios:</strong> Las inscripciones están sujetas a disponibilidad de cupos y se realizan hasta 2 días antes de la fecha elegida.
                          </p>
                          <p>
                            <strong>Cancelaciones:</strong> El parque se reserva el derecho de cancelar o reprogramar actividades por condiciones climáticas o razones de seguridad.
                          </p>
                          <p>
                            <strong>Aceptación:</strong> La participación en la actividad implica la aceptación total de estos términos y condiciones.
                          </p>
                        </div>
                        <DialogFooter>
                          <DialogClose asChild>
                            <Button type="button">Cerrar</Button>
                          </DialogClose>
                        </DialogFooter>
                      </DialogContent>
                    </Dialog>
                  </>
                )}
              </AccordionContent>
            </AccordionItem>
           </Accordion>
         </div> {/* Fin de la Columna 2 */}
        </CardContent>

        <CardFooter className="flex flex-col">
          <Button type="submit" className="w-full mt-4" disabled={!isFormValid() || isSubmitting}>
            {isSubmitting ? "Reserving..." : "Reserve My Spot"}
          </Button>
        </CardFooter>
      </form>
    </Card>
  )
}
