import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface User {
  id: number;
  username: string;
  email: string;
  role: string;
}

interface BookingState {
  user: User | null;
  token: string | null;
  vehicleId: string | null;
  pickupDate: string;
  returnDate: string;
  locationId: string;
  extras: string[];
  customerDetails: {
    firstName: string;
    lastName: string;
    email: string;
    phone: string;
    passportNumber: string;
  };
  step: number;
  setVehicle: (id: string) => void;
  setDates: (pickup: string, returnDate: string) => void;
  setLocation: (id: string) => void;
  toggleExtra: (extraId: string) => void;
  setCustomerDetails: (details: Partial<BookingState['customerDetails']>) => void;
  setStep: (step: number) => void;
  setAuth: (user: User | null, token: string | null) => void;
  reset: () => void;
}

export const useBookingStore = create<BookingState>()(
  persist(
    (set) => ({
      user: null,
      token: null,
      vehicleId: null,
      pickupDate: new Date().toISOString().split('T')[0],
      returnDate: new Date(Date.now() + 86400000).toISOString().split('T')[0],
      locationId: '',
      extras: [],
      customerDetails: {
        firstName: '',
        lastName: '',
        email: '',
        phone: '',
        passportNumber: '',
      },
      step: 1,

      setVehicle: (id) => set({ vehicleId: id }),
      setDates: (pickup, returnDate) => set({ pickupDate: pickup, returnDate: returnDate }),
      setLocation: (id) => set({ locationId: id }),
      toggleExtra: (extraId) => set((state) => ({
        extras: state.extras.includes(extraId)
          ? state.extras.filter(id => id !== extraId)
          : [...state.extras, extraId]
      })),
      setCustomerDetails: (details) => set((state) => ({
        customerDetails: { ...state.customerDetails, ...details }
      })),
      setStep: (step) => set({ step }),
      setAuth: (user, token) => set({ user, token }),
      reset: () => set({
        user: null,
        token: null,
        vehicleId: null,
        extras: [],
        step: 1,
        customerDetails: { firstName: '', lastName: '', email: '', phone: '', passportNumber: '' }
      }),
    }),
    {
      name: 'marrakech-drive-booking-storage',
    }
  )
);
